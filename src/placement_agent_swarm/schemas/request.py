from pydantic import BaseModel, ConfigDict, Field


class WorkflowRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    requested_output: str = Field(min_length=1)