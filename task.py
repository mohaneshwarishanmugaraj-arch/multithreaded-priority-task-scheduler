import time


class Task:

    def __init__(
        self,
        task_id,
        priority,
        weight,
        resource_units,
        execution_time
    ):

        # Task Details
        self.task_id = task_id
        self.priority = priority
        self.weight = weight
        self.resource_units = resource_units
        self.execution_time = execution_time

        # Time Information
        self.creation_time = time.time()
        self.start_time = None
        self.completion_time = None

        # Task State
        self.state = "CREATED"

    # ----------------------------------------
    # Start Task
    # ----------------------------------------

    def start(self):

        self.start_time = time.time()
        self.state = "RUNNING"

    # ----------------------------------------
    # Complete Task
    # ----------------------------------------

    def complete(self):

        self.completion_time = time.time()
        self.state = "COMPLETED"

    # ----------------------------------------
    # Waiting Time
    # ----------------------------------------

    def waiting_time(self):

        if self.start_time is None:
            return 0

        return self.start_time - self.creation_time

    # ----------------------------------------
    # Turnaround Time
    # ----------------------------------------

    def turnaround_time(self):

        if self.completion_time is None:
            return 0

        return self.completion_time - self.creation_time

    # ----------------------------------------
    # Display Task Information
    # ----------------------------------------

    def __str__(self):

        return (
            f"Task("
            f"ID={self.task_id}, "
            f"Priority={self.priority}, "
            f"Weight={self.weight}, "
            f"Resources={self.resource_units}, "
            f"Execution={self.execution_time}s, "
            f"State={self.state}"
            f")"
        )