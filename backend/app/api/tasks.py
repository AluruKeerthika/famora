
from datetime import date, datetime, time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.task import Task as TaskModel

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Structure of a new task
class TaskCreate(BaseModel):
    title: str
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None


# Structure of a task returned by the API
class TaskResponse(BaseModel):
    id: int
    title: str
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None
    completed: bool


# Create a task
@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = TaskModel(
        title=task_data.title,
        assigned_to=task_data.assigned_to,
        due_date=(
            datetime.combine(task_data.due_date, time.min)
            if task_data.due_date
            else None
        ),
        status="pending"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title,
        "assigned_to": new_task.assigned_to,
        "due_date": new_task.due_date.date() if new_task.due_date else None,
        "completed": new_task.status == "completed"
    }


# Get all tasks
@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()

    return [
        {
            "id": task.id,
            "title": task.title,
            "assigned_to": task.assigned_to,
            "due_date": task.due_date.date() if task.due_date else None,
            "completed": task.status == "completed"
        }
        for task in tasks
    ]


# Mark a task as completed
@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = "completed"

    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "title": task.title,
        "assigned_to": task.assigned_to,
        "due_date": task.due_date.date() if task.due_date else None,
        "completed": task.status == "completed"
    }
