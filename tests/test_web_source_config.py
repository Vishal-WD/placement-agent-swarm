import pytest
from pydantic import ValidationError

from placement_agent_swarm.config import WebSourceConfig


def test_web_source_config_uses_expected_defaults() -> None:
    config = WebSourceConfig()

    assert config.max_attempts == 3
    assert config.retry_delay_seconds == 1.0
    assert config.request_timeout_seconds == 10.0
    assert config.user_agent == "placement-agent-swarm/0.1"


def test_web_source_config_accepts_valid_custom_values() -> None:
    config = WebSourceConfig(
        max_attempts=5,
        retry_delay_seconds=0.5,
        request_timeout_seconds=6.0,
        user_agent="placement-agent-swarm-test/1.0",
    )

    assert config.max_attempts == 5
    assert config.retry_delay_seconds == 0.5
    assert config.request_timeout_seconds == 6.0
    assert config.user_agent == "placement-agent-swarm-test/1.0"


def test_web_source_config_cleans_user_agent() -> None:
    config = WebSourceConfig(
        user_agent="  placement-agent-swarm-test/1.0  ",
    )

    assert config.user_agent == "placement-agent-swarm-test/1.0"


def test_web_source_config_rejects_invalid_max_attempts() -> None:
    with pytest.raises(ValidationError):
        WebSourceConfig(max_attempts=0)


def test_web_source_config_rejects_negative_retry_delay() -> None:
    with pytest.raises(ValidationError):
        WebSourceConfig(retry_delay_seconds=-0.1)


def test_web_source_config_rejects_invalid_request_timeout() -> None:
    with pytest.raises(ValidationError):
        WebSourceConfig(request_timeout_seconds=0)


def test_web_source_config_rejects_empty_user_agent() -> None:
    with pytest.raises(ValidationError):
        WebSourceConfig(user_agent="   ")


def test_web_source_config_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        WebSourceConfig.model_validate(
            {
                "unknown_setting": True,
            }
        )


def test_web_source_config_is_immutable() -> None:
    config = WebSourceConfig()

    with pytest.raises(ValidationError):
        config.max_attempts = 5