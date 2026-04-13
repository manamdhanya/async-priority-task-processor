from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any


class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Status(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskCreate(BaseModel):
    payload: Dict[str, Any]
    priority: Priority


class TaskResponse(BaseModel):
    id: str
    payload: Dict[str, Any]
    priority: Priority
    status: Status
    retry_count: int