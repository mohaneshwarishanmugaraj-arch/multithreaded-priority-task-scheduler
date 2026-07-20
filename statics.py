# statistics.py

import threading


class Statistics:

    def __init__(self):

        self.lock = threading.Lock()

        self.total_tasks_produced = 0
        self.total_tasks_completed = 0

        self.high_completed = 0
        self.medium_completed = 0
        self.low_completed = 0

        self.total_waiting_time = 0
        self.total_turnaround_time = 0

        self.priority_promotions = 0

    # --------------------------------

    def task_produced(self):

        with self.lock:
            self.total_tasks_produced += 1

    # --------------------------------

    def task_completed(self, task):

        with self.lock:

            self.total_tasks_completed += 1

            if task.priority == "HIGH":
                self.high_completed += 1

            elif task.priority == "MEDIUM":
                self.medium_completed += 1

            else:
                self.low_completed += 1

            self.total_waiting_time += task.waiting_time()
            self.total_turnaround_time += task.turnaround_time()

    # --------------------------------

    def promoted(self):

        with self.lock:
            self.priority_promotions += 1

    # --------------------------------

    def print_statistics(self, scheduler, resource_manager):

        print("\n========== FINAL STATISTICS ==========\n")

        print("Total Tasks Produced :", self.total_tasks_produced)
        print("Total Tasks Completed:", self.total_tasks_completed)

        print("\nCompleted By Priority")
        print("----------------------")
        print("HIGH   :", self.high_completed)
        print("MEDIUM :", self.medium_completed)
        print("LOW    :", self.low_completed)

        if self.total_tasks_completed > 0:

            avg_wait = (
                self.total_waiting_time /
                self.total_tasks_completed
            )

            avg_turnaround = (
                self.total_turnaround_time /
                self.total_tasks_completed
            )

        else:

            avg_wait = 0
            avg_turnaround = 0

        print("\nAverage Waiting Time    :", round(avg_wait, 2))
        print("Average Turnaround Time :", round(avg_turnaround, 2))

        print("\nMaximum Queue Size :", scheduler.max_queue_size)

        print(
            "Resource Utilization :",
            round(resource_manager.utilization(), 2),
            "%"
        )

        print(
            "Priority Promotions :",
            self.priority_promotions
        )

        print("\n======================================")