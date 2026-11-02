"""Input and output validation for possessions."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PossessionFields(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    category: str | None = Field(default=None, max_length=100)
    attributes: dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def meaningful_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank")
        return value


class PossessionCreate(PossessionFields):
    model_config = ConfigDict(extra="forbid", strict=True)


class PossessionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    category: str | None = Field(default=None, max_length=100)
    attributes: dict[str, Any] | None = None

    @field_validator("name")
    @classmethod
    def meaningful_name(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Name cannot be null")
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank")
        return value

    @field_validator("attributes")
    @classmethod
    def attributes_not_null(cls, value: dict[str, Any] | None) -> dict[str, Any]:
        if value is None:
            raise ValueError("Attributes cannot be null")
        return value


class PossessionRead(PossessionFields):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime
