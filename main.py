# main.py

from configuration import (
    NUM_PRODUCERS,
    NUM_WORKERS,
    TOTAL_RESOURCES
)

from scheduler import Scheduler
from producer import Producer
from worker import Worker
from resource import ResourceManager
from logger import Logger
from statics import Statistics


def main():

    print("=" * 60)
    print(" MULTITHREADED PRIORITY TASK SCHEDULER ")
    print("=" * 60)

    # -----------------------------------
    # Create Shared Objects
    # -----------------------------------

    scheduler = Scheduler()

    logger = Logger()

    statistics = Statistics()

    resource_manager = ResourceManager(TOTAL_RESOURCES)

    # -----------------------------------
    # Create Producer Threads
    # -----------------------------------

    producers = []

    for i in range(NUM_PRODUCERS):

        producer = Producer(
            producer_id=i + 1,
            scheduler=scheduler,
            logger=logger,
            statistics=statistics
        )

        producers.append(producer)

    # -----------------------------------
    # Create Worker Threads
    # -----------------------------------

    workers = []

    for i in range(NUM_WORKERS):

        worker = Worker(
            worker_id=i + 1,
            scheduler=scheduler,
            resource_manager=resource_manager,
            logger=logger,
            statistics=statistics
        )

        workers.append(worker)

    # -----------------------------------
    # Start Producer Threads
    # -----------------------------------

    print("\nStarting Producer Threads...\n")

    for producer in producers:
        producer.start()

    # -----------------------------------
    # Start Worker Threads
    # -----------------------------------

    print("Starting Worker Threads...\n")

    for worker in workers:
        worker.start()

    # -----------------------------------
    # Wait for Producers to Finish
    # -----------------------------------

    for producer in producers:
        producer.join()

    print("\nAll Producers Finished.\n")

    # Tell scheduler that production is complete
    scheduler.finish_production()

    # Wake up waiting workers
    for _ in range(NUM_WORKERS):
        scheduler.available_tasks.release()

    # -----------------------------------
    # Wait for Workers to Finish
    # -----------------------------------

    for worker in workers:
        worker.join()

    print("\nAll Workers Finished.\n")

    # -----------------------------------
    # Print Final Statistics
    # -----------------------------------

    statistics.print_statistics(
        scheduler,
        resource_manager
    )

    print("\nProgram Executed Successfully.")


# ---------------------------------------
# Program Entry Point
# ---------------------------------------

if __name__ == "__main__":
    main()