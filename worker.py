# worker.py

import threading
import time


class Worker(threading.Thread):

    def __init__(
        self,
        worker_id,
        scheduler,
        resource_manager,
        logger,
        statistics
    ):

        super().__init__()

        self.worker_id = worker_id
        self.scheduler = scheduler
        self.resource_manager = resource_manager
        self.logger = logger
        self.statistics = statistics

    # ---------------------------------------
    # Worker Thread
    # ---------------------------------------

    def run(self):

        self.logger.log(f"Worker-{self.worker_id} Started")

        while True:

            # Get highest priority task
            task = self.scheduler.get_task()

            # Stop if production is finished and no tasks remain
            if task is None:

                if self.scheduler.production_finished:
                    break

                continue

            # Remove task from queue
            self.logger.queue_removed(task)

            # Request required resources
            self.resource_manager.acquire(task.resource_units)

            self.logger.resource_allocated(task)

            # Start execution
            task.start()

            self.logger.task_started(
                self.worker_id,
                task
            )

            # Simulate execution
            time.sleep(task.execution_time)

            # Complete task
            task.complete()

            # Release resources
            self.resource_manager.release(
                task.resource_units
            )

            self.logger.resource_released(task)

            self.logger.task_completed(
                self.worker_id,
                task
            )

            # Update statistics
            self.statistics.task_completed(task)

        self.logger.worker_finished(self.worker_id)