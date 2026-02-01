from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from .database import get_db, init_db, engine
from . import models, ai_engine

# Initialize DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Core Feeling API")

# --- Pydantic Schemas ---
class TaskCreate(BaseModel):
    title: str
    date: str = "Today"
    time: str = "Flexible"
    priority: str = "Medium"
    mood: Optional[str] = "Neutral"

class Task(TaskCreate):
    id: int
    completed: bool

    class Config:
        orm_mode = True

class Mission(BaseModel):
    mission_tasks: List[Task]
    quick_win: Optional[Task]
    optional_task: Optional[Task]

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Core Feeling Backend is Running"}

@app.get("/mission", response_model=Mission)
def get_daily_mission(db: Session = Depends(get_db)):
    """
    Returns the 'Daily Mission': 3 important tasks, 1 quick win, 1 optional.
    """
    # Logic: High priority first, then others
    tasks = db.query(models.Task).filter(models.Task.completed == False).all()
    
    # Sort by priority (Simple heuristic: High > Medium > Low)
    # real impl would use a proper sort key
    high_priority = [t for t in tasks if t.priority == "High"]
    medium_priority = [t for t in tasks if t.priority == "Medium"]
    low_priority = [t for t in tasks if t.priority == "Low"]
    
    sorted_tasks = high_priority + medium_priority + low_priority
    
    mission_tasks = sorted_tasks[:3]
    
    # Find a quick win (Low priority or just a short task)
    quick_win = None
    if low_priority:
        quick_win = low_priority[0]
    elif len(sorted_tasks) > 3:
         quick_win = sorted_tasks[3]

    optional = sorted_tasks[4] if len(sorted_tasks) > 4 else None

    return {
        "mission_tasks": mission_tasks,
        "quick_win": quick_win,
        "optional_task": optional
    }

@app.post("/tasks/magic_add", response_model=Task)
def magic_add(user_input: str, db: Session = Depends(get_db)):
    """
    Simulates AI parsing of a user string into a structured task.
    """
    # Use AI Engine
    parsed_data = ai_engine.AIEngine.parse_task_input(user_input)
    
    db_task = models.Task(
        title=parsed_data["title"],
        date=parsed_data["date"],
        time=parsed_data["time"],
        priority=parsed_data["priority"],
        mood=parsed_data["mood"]
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
