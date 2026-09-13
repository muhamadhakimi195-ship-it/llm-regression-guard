from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Category = Literal["billing", "technical", "account", "general"]

class EmailInput(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        str_strip_whitespace=True,
        )

    text: str = Field(min_length=1, max_length=20_000)

class EmailResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        str_strip_whitespace=True,

    
        )
    
    category: Category
    summary: str = Field(min_length=5, max_length=300)


