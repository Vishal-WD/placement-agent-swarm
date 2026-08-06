from pydantic import BaseModel, ConfigDict, Field, field_validator

DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_RETRY_DELAY_SECONDS = 1.0
DEFAULT_REQUEST_TIMEOUT_SECONDS = 10.0
DEFAULT_USER_AGENT = "placement-agent-swarm/0.1"


class WebSourceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_attempts: int = Field(
        default=DEFAULT_MAX_ATTEMPTS,
        ge=1,
    )
    retry_delay_seconds: float = Field(
        default=DEFAULT_RETRY_DELAY_SECONDS,
        ge=0,
    )
    request_timeout_seconds: float = Field(
        default=DEFAULT_REQUEST_TIMEOUT_SECONDS,
        gt=0,
    )
    user_agent: str = DEFAULT_USER_AGENT

    @field_validator("user_agent")
    @classmethod
    def validate_user_agent(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("user_agent cannot be empty")

        return cleaned_value