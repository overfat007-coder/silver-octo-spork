from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    login: str
    password: str


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class TeamMemberAdd(BaseModel):
    user_id: int | None = None
    email: EmailStr | None = None


class TeamRoleUpdate(BaseModel):
    role: str


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = ""
    due_date: datetime | None = None
    project_id: int | None = None
    team_id: int | None = None
    assignee_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    due_date: datetime | None = None
    is_completed: bool | None = None
    assignee_id: int | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: int
    is_completed: bool
    category: str | None
    estimated_minutes: int | None
    due_date: datetime | None
    team_id: int | None
    predicted_completion_time: int | None = None
    overdue_probability: float | None = None
    is_risky: bool = False


class NotificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    message: str
    is_read: bool
    created_at: datetime


class ProductivityAnalytics(BaseModel):
    completed_week: int
    completed_month: int
    by_category: dict[str, int]
    total_estimated_minutes_open: int


class TaskRelationCreate(BaseModel):
    target_task_id: int
    relation_type: str


class TaskRelationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_task_id: int
    target_task_id: int
    relation_type: str


class ExperimentStartRequest(BaseModel):
    name: str = "ml_predictions_visibility"
