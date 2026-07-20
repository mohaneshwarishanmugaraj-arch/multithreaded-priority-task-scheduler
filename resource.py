# resource.py

import threading


class ResourceManager:

    def __init__(self, total_resources):

        self.total_resources = total_resources
        self.available_resources = total_resources

        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def acquire(self, units):

        with self.condition:

            while self.available_resources < units:
                self.condition.wait()

            self.available_resources -= units

    def release(self, units):

        with self.condition:

            self.available_resources += units

            self.condition.notify_all()

    def utilization(self):

        used = self.total_resources - self.available_resources

        return (used / self.total_resources) * 100