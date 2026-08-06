from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class SourceType(StrEnum):
    OFFICIAL_DOCUMENTATION = "official_documentation"
    OFFICIAL_LEARNING_RESOURCE = "official_learning_resource"


class CollectedSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    url: HttpUrl
    source_type: SourceType
    content: str = Field(min_length=1)