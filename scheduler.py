# scheduler.py

import threading
import time
from collections import deque
from configuration import HIGH, MEDIUM, LOW, BUFFER_SIZE, AGING_TIME


class Scheduler:

    def __init__(self):

        # -----------------------------
        # Priority Queues
        # -----------------------------
        self.high_queue = deque()
        self.medium_queue = deque()
        self.low_queue = deque()

        # -----------------------------
        # Mutex Lock
        # Protects all queues
        # -----------------------------
        self.lock = threading.Lock()

        # -----------------------------
        # Semaphores
        # -----------------------------

        # Number of empty slots in buffer
        self.empty_slots = threading.Semaphore(BUFFER_SIZE)

        # Number of available tasks
        self.available_tasks = threading.Semaphore(0)

        # -----------------------------
        # Statistics
        # -----------------------------
        self.max_queue_size = 0

        # Indicates all producers are done
        self.production_finished = False

    # =========================================================
    # Add Task
    # =========================================================
    def add_task(self, task):

        # Wait if buffer is full
        self.empty_slots.acquire()

        with self.lock:

            task.state = 'QUEUED'

            if task.priority == HIGH:
                self.high_queue.append(task)

            elif task.priority == MEDIUM:
                self.medium_queue.append(task)

            else:
                self.low_queue.append(task)

            # Track maximum queue size
            current_size = self.total_tasks()

            if current_size > self.max_queue_size:
                self.max_queue_size = current_size

        # Notify one waiting worker
        self.available_tasks.release()

    # =========================================================
    # Get Next Task
    # =========================================================
    def get_task(self):

        # Wait until a task is available
        self.available_tasks.acquire()

        with self.lock:

            # Check if scheduler is completely finished
            if self.production_finished and self.total_tasks() == 0:
                return None

            # Promote old tasks before selection
            self.promote_waiting_tasks()

            task = None

            # HIGH priority first
            if self.high_queue:
                task = self.select_weighted_task(self.high_queue)

            # Then MEDIUM
            elif self.medium_queue:
                task = self.select_weighted_task(self.medium_queue)

            # Then LOW
            elif self.low_queue:
                task = self.select_weighted_task(self.low_queue)

        # One buffer slot becomes free
        self.empty_slots.release()

        return task

    # =========================================================
    # Weighted Scheduling
    # Higher weight gets preference
    # =========================================================
    def select_weighted_task(self, queue):

        if not queue:
            return None

        # Find task with highest weight
        selected_index = 0
        highest_weight = queue[0].weight

        for i in range(1, len(queue)):

            if queue[i].weight > highest_weight:
                highest_weight = queue[i].weight
                selected_index = i

        # NOTE: queue is a collections.deque, and deque.pop() does NOT
        # accept an index argument (unlike list.pop()). Grab the task
        # by index, then delete it by index instead.
        selected_task = queue[selected_index]
        del queue[selected_index]

        return selected_task

    # =========================================================
    # Aging / Starvation Prevention
    # =========================================================
    def promote_waiting_tasks(self):

        current_time = time.time()

        # LOW -> MEDIUM
        self.promote_queue(
            self.low_queue,
            MEDIUM,
            current_time
        )

        # MEDIUM -> HIGH
        self.promote_queue(
            self.medium_queue,
            HIGH,
            current_time
        )

    # =========================================================
    # Helper for Promotion
    # =========================================================
    def promote_queue(self, queue, new_priority, current_time):

        promoted_tasks = []

        for task in list(queue):

            waiting_time = current_time - task.creation_time

            if waiting_time >= AGING_TIME:

                queue.remove(task)

                task.priority = new_priority
                task.state = 'PROMOTED'

                promoted_tasks.append(task)

        # Insert into new queue
        for task in promoted_tasks:

            if new_priority == HIGH:
                self.high_queue.append(task)

            elif new_priority == MEDIUM:
                self.medium_queue.append(task)

    # =========================================================
    # Total Tasks
    # =========================================================
    def total_tasks(self):

        return (
            len(self.high_queue) +
            len(self.medium_queue) +
            len(self.low_queue)
        )

    # =========================================================
    # Queue Status
    # =========================================================
    def queue_status(self):

        with self.lock:

            return {
                'HIGH': len(self.high_queue),
                'MEDIUM': len(self.medium_queue),
                'LOW': len(self.low_queue),
                'TOTAL': self.total_tasks()
            }

    # =========================================================
    # Check if Empty
    # =========================================================
    def is_empty(self):

        with self.lock:
            return self.total_tasks() == 0

    # =========================================================
    # Mark Production Finished
    # =========================================================
    def finish_production(self):

        self.production_finished = True
