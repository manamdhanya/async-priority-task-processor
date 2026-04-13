from fastapi import FastAPI, HTTPException
from app.models import TaskCreate, TaskResponse, Status
from app.tasks import process_high, process_medium, process_low
from app.db import task_collection
import uuid

app = FastAPI()


# 1. Create Task
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    task_id = str(uuid.uuid4())

    new_task = {
        "_id": task_id,
        "payload": task.payload,
        "priority": task.priority,
        "status": Status.PENDING,
        "retry_count": 0,
    }

    task_collection.insert_one(new_task)

    if task.priority == "HIGH":
        process_high.delay(task_id)
    elif task.priority == "MEDIUM":
        process_medium.delay(task_id)
    else:
        process_low.delay(task_id)

    return {
        "id": task_id,
        "payload": task.payload,
        "priority": task.priority,
        "status": Status.PENDING,
        "retry_count": 0,
    }


# 2. Get Task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    task = task_collection.find_one({"_id": task_id})

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": task["_id"],
        "payload": task["payload"],
        "priority": task["priority"],
        "status": task["status"],
        "retry_count": task["retry_count"],
    }


# 3. List Tasks with Filters
@app.get("/tasks")
def list_tasks(status: str = None, priority: str = None):
    query = {}

    if status:
        query["status"] = status

    if priority:
        query["priority"] = priority

    tasks = list(task_collection.find(query))

    return [
        {
            "id": task["_id"],
            "payload": task["payload"],
            "priority": task["priority"],
            "status": task["status"],
            "retry_count": task["retry_count"],
        }
        for task in tasks
    ]