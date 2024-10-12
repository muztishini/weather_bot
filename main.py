import uvicorn
from fastapi import FastAPI, HTTPException
from models import Log, SessionLocal
from typing import Optional
from datetime import datetime

app = FastAPI()
db = SessionLocal()


@app.get("/logs")
def get_logs(skip: int = 0, limit: int = 10, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
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


@app.get("/logs/{user_id}")
def get_user_logs(user_id: str, skip: int = 0, limit: int = 10, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
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
        raise HTTPException(status_code=404, detail="Logs not found for this user")
    return logs


if __name__ == "__main__":
    uvicorn.run(app)
