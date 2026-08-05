from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class CollectedSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    url: HttpUrl
    source_type: str = Field(min_length=1)
    content: str = Field(min_length=1)