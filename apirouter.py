from fastapi import APIRouter, HTTPException
from models import Log, SessionLocal
from typing import Optional
from datetime import datetime


db = SessionLocal()
apirouter = APIRouter()


@apirouter.get("/logs")
async def get_logs(skip: int = 0, limit: int = 10, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    """
    Возвращает список всех запросов с информацией о пользователе и времени запроса.
    """
    query = db.query(Log)

    if start_time:
        query = query.filter(Log.datatime >= start_time)
    if end_time:
        query = query.filter(Log.datatime <= end_time)

    logs = query.offset(skip).limit(limit).all()
    return logs


@apirouter.get("/logs/{user_id}")
async def get_user_logs(user_id: int, skip: int = 0, limit: int = 10, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    """
    Возвращает запросы конкретного пользователя.
    """
    query = db.query(Log)

    if start_time:
        query = query.filter(Log.datatime >= start_time)
    if end_time:
        query = query.filter(Log.datatime <= end_time)

    logs = query.filter(Log.userid == user_id).offset(skip).limit(limit).all()
    if not logs:
        raise HTTPException(status_code=404, detail="Логи не найдены для этого пользователя")
    return logs
