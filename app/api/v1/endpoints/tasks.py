from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.database import get_db 
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (
    create_task, get_user_tasks, get_task_by_id, update_task, delete_task
)

router = APIRouter()

@router.post("/", response_model = TaskResponse, status_code = status.HTTP_201_CREATED)
async def create(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),):
    return await create_task(db, task_data, current_user.id)

@router.get("/", response_model = list[TaskResponse])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    return await get_user_tasks(db, current_user.id)

@router.get("/{task_id}", response_model = TaskResponse)
async def get_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):

    task = await get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail = "Task not found")
    return task

@router.patch("/{task_id}", response_model = TaskResponse)
async def update(
    task_id: str,
    update_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    task = await get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "task not found")
    return await update_task(db, task, update_data)

@router.delete("/{task_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    task = await get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "task not found")
    await delete_task(db, task)



