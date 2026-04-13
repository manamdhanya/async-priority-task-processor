from app.celery_worker import celery
from app.db import task_collection
from app.models import Status
import random
import time


def update_status(task_id, status):
    task_collection.update_one(
        {"_id": task_id},
        {"$set": {"status": status}}
    )


@celery.task(bind=True, max_retries=3)
def process_high(self, task_id):
    print(f" HIGH task received: {task_id}")
    process(self, task_id, "HIGH")


@celery.task(bind=True, max_retries=3)
def process_medium(self, task_id):
    print(f" MEDIUM task received: {task_id}")
    process(self, task_id, "MEDIUM")


@celery.task(bind=True, max_retries=3)
def process_low(self, task_id):
    print(f" LOW task received: {task_id}")
    process(self, task_id, "LOW")


def process(self, task_id, priority):
    task = task_collection.find_one({"_id": task_id})

    # Idempotency check
    if task["status"] == Status.COMPLETED:
        print(f" Already completed: {task_id}")
        return

    # Atomic update (concurrency safe)
    updated = task_collection.find_one_and_update(
        {"_id": task_id, "status": Status.PENDING},
        {"$set": {"status": Status.PROCESSING}}
    )

    if not updated:
        print(f" Skipped (already taken): {task_id}")
        return

    print(f" Processing {priority} task: {task_id}")

    time.sleep(5)

    if random.random() < 0.3:
        print(f" Failed {priority} task: {task_id} (retrying)")
        task_collection.update_one(
            {"_id": task_id},
            {"$inc": {"retry_count": 1}}
        )
        raise self.retry(countdown=5)

    # Success
    print(f" Completed {priority} task: {task_id}")
    update_status(task_id, Status.COMPLETED)