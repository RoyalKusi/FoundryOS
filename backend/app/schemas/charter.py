from pydantic import BaseModel

class OKR(BaseModel):
    objective: str
    keyResults: list[str]
    ownerRoleHint: str | None = None
    dueAt: str | None = None

class Constraints(BaseModel):
    budget: str | None = None
    headcount: str | None = None
    regulations: list[str] | None = None

class Cadence(BaseModel):
    standupTime: str = "08:00"
    weeklyReportDay: str = "Friday"
    weeklyReportTime: str = "16:00"

class CharterSchema(BaseModel):
    mission: str
    vision: str
    values: list[str]
    okrs: list[OKR]
    constraints: Constraints | None = None
    cadence: Cadence | None = None
