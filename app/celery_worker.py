from celery import Celery

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.autodiscover_tasks(["app"])

# Priority queues
celery.conf.task_routes = {
    "app.tasks.process_high": {"queue": "high"},
    "app.tasks.process_medium": {"queue": "medium"},
    "app.tasks.process_low": {"queue": "low"},
}

celery.conf.task_acks_late = True
celery.conf.worker_prefetch_multiplier = 1