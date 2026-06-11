import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

from app.db.redis import redis_client

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
    
    cache_key = f"task:{task_id}:{user_id}"

    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if task:
        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "result": task.result,
            "user_id": task.user_id,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }
        await redis_client.setex(cache_key, 300, json.dumps(task_data))

    return task

async def update_task(db: AsyncSession, task: Task, update_data: TaskUpdate) -> Task:
    if update_data.status is not None:
        task.status = update_data.status
    if update_data.result is not None:
        task.result = update_data.result

    await db.flush()

    cache_key = f"task:{task.id}:{task.user_id}"
    await redis_client.delete(cache_key)

    return task

async def delete_task(db: AsyncSession, task: Task) -> None:
    cache_key = f"task:{task.id}:{task.user_id}"
    await redis_client.delete(cache_key)
    await db.delete(task)
    await db.flush()

