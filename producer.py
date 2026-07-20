# producer.py

import threading
import random
import time

from task import Task

from configuration import (
    HIGH,
    MEDIUM,
    LOW,
    TASKS_PER_PRODUCER,
    MIN_WEIGHT,
    MAX_WEIGHT,
    MIN_RESOURCE_UNITS,
    MAX_RESOURCE_UNITS,
    MIN_EXECUTION_TIME,
    MAX_EXECUTION_TIME
)


class Producer(threading.Thread):

    # Shared Task ID Counter
    task_counter = 1
    counter_lock = threading.Lock()

    def __init__(self, producer_id, scheduler, logger, statistics):

        super().__init__()

        self.producer_id = producer_id
        self.scheduler = scheduler
        self.logger = logger
        self.statistics = statistics

    # -----------------------------------------
    # Create a New Task
    # -----------------------------------------

    def create_task(self):

        priority = random.choice([HIGH, MEDIUM, LOW])

        weight = random.randint(
            MIN_WEIGHT,
            MAX_WEIGHT
        )

        resource_units = random.randint(
            MIN_RESOURCE_UNITS,
            MAX_RESOURCE_UNITS
        )

        execution_time = random.randint(
            MIN_EXECUTION_TIME,
            MAX_EXECUTION_TIME
        )

        with Producer.counter_lock:

            task_id = Producer.task_counter
            Producer.task_counter += 1

        task = Task(
            task_id=task_id,
            priority=priority,
            weight=weight,
            resource_units=resource_units,
            execution_time=execution_time
        )

        return task

    # -----------------------------------------
    # Producer Thread
    # -----------------------------------------

    def run(self):

        self.logger.log(
            f"Producer-{self.producer_id} Started"
        )

        for _ in range(TASKS_PER_PRODUCER):

            task = self.create_task()

            self.statistics.task_produced()

            self.logger.log(
                f"Producer-{self.producer_id} Created Task-{task.task_id}"
            )

            self.scheduler.add_task(task)

            self.logger.log(
                f"Task-{task.task_id} inserted into {task.priority} Queue"
            )

            # Small delay to simulate real task generation
            time.sleep(random.uniform(0.2, 0.8))

        self.logger.log(
            f"Producer-{self.producer_id} Finished"
        )