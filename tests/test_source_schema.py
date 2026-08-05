import pytest
from pydantic import ValidationError

from placement_agent_swarm.schemas.source import CollectedSource


def test_collected_source_accepts_valid_data() -> None:
    source = CollectedSource.model_validate(
        {
            "title": "Python Documentation",
            "url": "https://docs.python.org/3/",
            "source_type": "official_documentation",
            "content": "Python is a programming language.",
        }
    )

    assert source.title == "Python Documentation"
    assert str(source.url) == "https://docs.python.org/3/"
    assert source.source_type == "official_documentation"
    assert source.content == "Python is a programming language."


def test_collected_source_rejects_invalid_url() -> None:
    invalid_data: dict[str, object] = {
        "title": "Invalid Source",
        "url": "not-a-valid-url",
        "source_type": "website",
        "content": "Some content",
    }

    with pytest.raises(ValidationError):
        CollectedSource.model_validate(invalid_data)


def test_collected_source_rejects_empty_content() -> None:
    invalid_data: dict[str, object] = {
        "title": "Empty Source",
        "url": "https://example.com/",
        "source_type": "website",
        "content": "",
    }

    with pytest.raises(ValidationError):
        CollectedSource.model_validate(invalid_data)


def test_collected_source_rejects_extra_fields() -> None:
    invalid_data: dict[str, object] = {
        "title": "Example Source",
        "url": "https://example.com/",
        "source_type": "website",
        "content": "Example content",
        "unexpected_field": "not allowed",
    }

    with pytest.raises(ValidationError):
        CollectedSource.model_validate(invalid_data)