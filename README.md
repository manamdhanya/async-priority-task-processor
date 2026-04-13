# Async Priority Task Processing System

## Overview

This project implements a **backend system for asynchronous task processing** with priority-based scheduling, retries, and concurrency handling.

It is designed to simulate real-world distributed systems using queues and background workers.


## Tech Stack

* **FastAPI** – REST API
* **MongoDB (Atlas)** – Database
* **Redis** – Message broker
* **Celery** – Asynchronous task queue

---

## Features

### Task Management APIs

* Create Task (`POST /tasks`)
* Get Task Status (`GET /tasks/{id}`)
* List Tasks with Filters (`GET /tasks`)

### Priority Handling

* Tasks are routed into separate queues:

  * HIGH
  * MEDIUM
  * LOW
* Priority is enforced at queue level (**HIGH > MEDIUM > LOW**)


### Asynchronous Processing

* Tasks are processed by Celery workers in the background
* Multiple workers allow parallel execution

---

### Retry Mechanism

* ~30% simulated failure using randomness
* Automatic retry up to 3 times
* Retry delay implemented

### Concurrency Handling

* Atomic database updates ensure:

  * No duplicate processing
  * No race conditions

### Idempotency

* Tasks are checked before execution
* Already completed tasks are skipped

### Worker Crash Recovery

* Celery ensures re-delivery of unacknowledged tasks
* Guarantees **at-least-once execution**

## System Design

### Architecture Flow

1. Client sends task → FastAPI
2. Task stored in MongoDB
3. Task sent to Redis queue via Celery
4. Worker consumes task
5. Status updated in DB

## Important Notes

* Priority is applied at **task scheduling level**
* Running tasks are **not preempted**
* Multiple workers improve scalability

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Redis

```bash
brew services start redis
```

### 3. Start FastAPI

```bash
uvicorn app.main:app --reload
```

### 4. Start Workers (recommended)

```bash
celery -A app.celery_worker worker -Q high --loglevel=info
celery -A app.celery_worker worker -Q medium --loglevel=info
celery -A app.celery_worker worker -Q low --loglevel=info
```

## Environment Variables

Create a `.env` file:

```env
MONGO_URI=your_mongodb_connection_string
```

## 📊 Task Lifecycle

```text
PENDING → PROCESSING → COMPLETED / FAILED
```

## 💡 Trade-offs

* No preemption of running tasks
* Priority enforced via queues instead of dynamic scheduling
* Simpler architecture over complex scheduling systems

## Conclusion

This system demonstrates:

* Distributed task processing
* Queue-based architecture
* Reliable and scalable backend design
