from pydantic import BaseModel, Field

class CharterPromptOutput(BaseModel):
    mission: str = Field(description="Mission statement")
    vision: str = Field(description="Vision statement")
    values: list[str]
