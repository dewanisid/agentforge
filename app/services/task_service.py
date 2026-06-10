from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: str) -> Task:
    task = Task(
        title = task_data.title,
        description = task_data.description,
        user_id = user_id,
    )
    db.add(task)
    await db.flush()
    return task

async def get_user_tasks(db: AsyncSession, user_id: str) -> list[Task]:
    result = await db.execute(select(Task).where(Task.user_id == user_id))
    return list(result.scalars().all())


async def get_task_by_id(db: AsyncSession, task_id: str, user_id: str) -> Task:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def update_task(db: AsyncSession, task: Task, update_data: TaskUpdate) -> Task:
    if update_data.status is not None:
        task.status = update_data.status
    if update_data.result is not None:
        task.result = update_data.result

    await db.flush()
    return task

async def delete_task(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.flush()

