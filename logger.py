# logger.py

import threading
from datetime import datetime


class Logger:

    def __init__(self):
        # Mutex Lock for thread-safe logging
        self.lock = threading.Lock()

    def log(self, message):
        """
        Print thread-safe log message with timestamp.
        """

        with self.lock:

            current_time = datetime.now().strftime("%H:%M:%S")

            print(f"[{current_time}] {message}")

    # ------------------------------------------
    # Task Creation
    # ------------------------------------------

    def task_created(self, task):

        self.log(
            f"Task-{task.task_id} Created | "
            f"Priority={task.priority} | "
            f"Weight={task.weight}"
        )

    # ------------------------------------------
    # Queue Insertion
    # ------------------------------------------

    def queue_inserted(self, task):

        self.log(
            f"Task-{task.task_id} inserted into "
            f"{task.priority} Queue"
        )

    # ------------------------------------------
    # Queue Removal
    # ------------------------------------------

    def queue_removed(self, task):

        self.log(
            f"Task-{task.task_id} removed from "
            f"{task.priority} Queue"
        )

    # ------------------------------------------
    # Priority Promotion
    # ------------------------------------------

    def priority_promoted(self, task, old_priority):

        self.log(
            f"Task-{task.task_id} promoted "
            f"from {old_priority} to {task.priority}"
        )

    # ------------------------------------------
    # Resource Allocation
    # ------------------------------------------

    def resource_allocated(self, task):

        self.log(
            f"Allocated {task.resource_units} "
            f"resource unit(s) to Task-{task.task_id}"
        )

    # ------------------------------------------
    # Task Execution
    # ------------------------------------------

    def task_started(self, worker_id, task):

        self.log(
            f"Worker-{worker_id} started "
            f"Task-{task.task_id}"
        )

    # ------------------------------------------
    # Resource Release
    # ------------------------------------------

    def resource_released(self, task):

        self.log(
            f"Released {task.resource_units} "
            f"resource unit(s) from Task-{task.task_id}"
        )

    # ------------------------------------------
    # Task Completion
    # ------------------------------------------

    def task_completed(self, worker_id, task):

        self.log(
            f"Worker-{worker_id} completed "
            f"Task-{task.task_id}"
        )

    # ------------------------------------------
    # Producer Finished
    # ------------------------------------------

    def producer_finished(self, producer_id):

        self.log(
            f"Producer-{producer_id} Finished"
        )

    # ------------------------------------------
    # Worker Finished
    # ------------------------------------------

    def worker_finished(self, worker_id):

        self.log(
            f"Worker-{worker_id} Finished"
        )