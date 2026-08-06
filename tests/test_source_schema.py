import pytest
from pydantic import ValidationError

from placement_agent_swarm.schemas.source import (
    CollectedSource,
    SourceType,
)


def test_collected_source_accepts_valid_data() -> None:
    source = CollectedSource.model_validate(
        {
            "title": "Python Documentation",
            "url": "https://docs.python.org/3/",
            "source_type": SourceType.OFFICIAL_DOCUMENTATION,
            "content": "Python is a programming language.",
        }
    )

    assert source.title == "Python Documentation"
    assert str(source.url) == "https://docs.python.org/3/"
    assert source.source_type == SourceType.OFFICIAL_DOCUMENTATION
    assert source.content == "Python is a programming language."


def test_collected_source_accepts_valid_source_type_string() -> None:
    source = CollectedSource.model_validate(
        {
            "title": "Learning Resource",
            "url": "https://example.com/learning",
            "source_type": "official_learning_resource",
            "content": "Learning resource content.",
        }
    )

    assert source.source_type == SourceType.OFFICIAL_LEARNING_RESOURCE


def test_collected_source_rejects_invalid_url() -> None:
    invalid_data: dict[str, object] = {
        "title": "Invalid Source",
        "url": "not-a-valid-url",
        "source_type": SourceType.OFFICIAL_DOCUMENTATION,
        "content": "Some content",
    }

    with pytest.raises(ValidationError):
        CollectedSource.model_validate(invalid_data)


def test_collected_source_rejects_invalid_source_type() -> None:
    invalid_data: dict[str, object] = {
        "title": "Invalid Source Type",
        "url": "https://example.com/",
        "source_type": "website",
        "content": "Some content",
    }

    with pytest.raises(
        ValidationError,
        match=(
            "Input should be "
            "'official_documentation' or "
            "'official_learning_resource'"
        ),
    ):
        CollectedSource.model_validate(invalid_data)


def test_collected_source_rejects_empty_content() -> None:
    invalid_data: dict[str, object] = {
        "title": "Empty Source",
        "url": "https://example.com/",
        "source_type": SourceType.OFFICIAL_DOCUMENTATION,
        "content": "",
    }

    with pytest.raises(ValidationError):
        CollectedSource.model_validate(invalid_data)


def test_collected_source_rejects_extra_fields() -> None:
    invalid_data: dict[str, object] = {
        "title": "Example Source",
        "url": "https://example.com/",
        "source_type": SourceType.OFFICIAL_DOCUMENTATION,
        "content": "Example content",
        "unexpected_field": "not allowed",
    }

    with pytest.raises(ValidationError):
        CollectedSource.model_validate(invalid_data)


def test_collected_source_is_immutable() -> None:
    source = CollectedSource.model_validate(
        {
            "title": "Python Documentation",
            "url": "https://docs.python.org/3/",
            "source_type": SourceType.OFFICIAL_DOCUMENTATION,
            "content": "Python is a programming language.",
        }
    )

    with pytest.raises(ValidationError):
        source.title = "Changed Title"