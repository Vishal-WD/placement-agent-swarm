import pytest
from pydantic import ValidationError

from placement_agent_swarm.config import (
    APPROVED_SOURCES,
    SourceDefinition,
)


def test_approved_sources_contains_expected_domains() -> None:
    assert "communication" in APPROVED_SOURCES
    assert "java" in APPROVED_SOURCES


def test_each_domain_contains_multiple_sources() -> None:
    assert len(APPROVED_SOURCES["communication"]) >= 2
    assert len(APPROVED_SOURCES["java"]) >= 2


def test_all_registry_entries_are_source_definitions() -> None:
    for sources in APPROVED_SOURCES.values():
        for source in sources:
            assert isinstance(source, SourceDefinition)


def test_all_registry_sources_have_valid_values() -> None:
    for domain, sources in APPROVED_SOURCES.items():
        assert domain.strip()

        for source in sources:
            assert source.title.strip()
            assert str(source.url).startswith(("http://", "https://"))
            assert source.source_type.strip()


def test_source_definition_is_immutable() -> None:
    source = APPROVED_SOURCES["communication"][0]

    with pytest.raises(ValidationError):
        source.title = "Changed Title"


def test_approved_source_collections_are_immutable_tuples() -> None:
    for sources in APPROVED_SOURCES.values():
        assert isinstance(sources, tuple)


def test_approved_sources_mapping_is_immutable() -> None:
    mutable_view = APPROVED_SOURCES  # type: ignore[assignment]

    with pytest.raises(TypeError):
        mutable_view["python"] = ()  # type: ignore[index]