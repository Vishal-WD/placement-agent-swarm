from unittest.mock import MagicMock, patch

from placement_agent_swarm.connectors.web_source import (
    extract_text_from_html,
    fetch_web_source,
)


def test_fetch_web_source_returns_cleaned_collected_source() -> None:
    mock_response = MagicMock()
    mock_response.read.return_value = (
        b"<html><body><h1>Grammar Guide</h1>"
        b"<p>Subject-verb agreement content</p></body></html>"
    )
    mock_response.__enter__.return_value = mock_response
    mock_response.__exit__.return_value = False

    with patch(
        "placement_agent_swarm.connectors.web_source.urlopen",
        return_value=mock_response,
    ) as mock_urlopen:
        source = fetch_web_source(
            url="https://example.com/grammar",
            title="Grammar Guide",
            source_type="website",
        )

    assert source.title == "Grammar Guide"
    assert str(source.url) == "https://example.com/grammar"
    assert source.source_type == "website"
    assert source.content == (
        "Grammar Guide Subject-verb agreement content"
    )
    assert "<html>" not in source.content
    assert "<p>" not in source.content

    mock_urlopen.assert_called_once()


def test_extract_text_from_html_removes_tags() -> None:
    html = (
        "<html><head><title>Grammar</title></head>"
        "<body><h1>Subject-Verb Agreement</h1>"
        "<p>The verb must agree with the subject.</p></body></html>"
    )

    result = extract_text_from_html(html)

    assert result == (
        "Grammar Subject-Verb Agreement "
        "The verb must agree with the subject."
    )