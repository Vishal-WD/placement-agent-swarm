from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest

from placement_agent_swarm.connectors.web_source import (
    WebSourceFetchError,
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


def test_fetch_web_source_converts_url_error() -> None:
    with (
        patch(
            "placement_agent_swarm.connectors.web_source.urlopen",
            side_effect=URLError("Connection failed"),
        ),
        patch(
            "placement_agent_swarm.connectors.web_source.sleep"
        ) as mock_sleep,
        pytest.raises(
            WebSourceFetchError,
            match=(
                "Failed to fetch web source after "
                "3 attempts: Grammar Guide"
            ),
        ) as error_info,
    ):
        fetch_web_source(
            url="https://example.com/grammar",
            title="Grammar Guide",
            source_type="website",
        )

    assert isinstance(error_info.value.__cause__, URLError)
    assert mock_sleep.call_count == 2


def test_fetch_web_source_converts_timeout_error() -> None:
    with (
        patch(
            "placement_agent_swarm.connectors.web_source.urlopen",
            side_effect=TimeoutError("Request timed out"),
        ),
        patch(
            "placement_agent_swarm.connectors.web_source.sleep"
        ) as mock_sleep,
        pytest.raises(
            WebSourceFetchError,
            match=(
                "Failed to fetch web source after "
                "3 attempts: Grammar Guide"
            ),
        ) as error_info,
    ):
        fetch_web_source(
            url="https://example.com/grammar",
            title="Grammar Guide",
            source_type="website",
        )

    assert isinstance(error_info.value.__cause__, TimeoutError)
    assert mock_sleep.call_count == 2


def test_fetch_web_source_retries_then_succeeds() -> None:
    mock_response = MagicMock()
    mock_response.read.return_value = (
        b"<html><body><p>Recovered content</p></body></html>"
    )
    mock_response.__enter__.return_value = mock_response
    mock_response.__exit__.return_value = False

    with (
        patch(
            "placement_agent_swarm.connectors.web_source.urlopen",
            side_effect=[
                URLError("Temporary failure"),
                mock_response,
            ],
        ) as mock_urlopen,
        patch(
            "placement_agent_swarm.connectors.web_source.sleep"
        ) as mock_sleep,
    ):
        source = fetch_web_source(
            url="https://example.com/retry",
            title="Retry Source",
            source_type="website",
            max_attempts=2,
            retry_delay_seconds=0.5,
        )

    assert source.title == "Retry Source"
    assert source.content == "Recovered content"
    assert mock_urlopen.call_count == 2
    mock_sleep.assert_called_once_with(0.5)


def test_fetch_web_source_exhausts_all_attempts() -> None:
    with (
        patch(
            "placement_agent_swarm.connectors.web_source.urlopen",
            side_effect=URLError("Persistent failure"),
        ) as mock_urlopen,
        patch(
            "placement_agent_swarm.connectors.web_source.sleep"
        ) as mock_sleep,
        pytest.raises(
            WebSourceFetchError,
            match=(
                "Failed to fetch web source after "
                "3 attempts: Retry Source"
            ),
        ) as error_info,
    ):
        fetch_web_source(
            url="https://example.com/retry",
            title="Retry Source",
            source_type="website",
            max_attempts=3,
            retry_delay_seconds=0.25,
        )

    assert mock_urlopen.call_count == 3
    assert mock_sleep.call_count == 2
    mock_sleep.assert_called_with(0.25)
    assert isinstance(error_info.value.__cause__, URLError)


def test_fetch_web_source_rejects_invalid_max_attempts() -> None:
    with pytest.raises(
        ValueError,
        match="max_attempts must be at least 1",
    ):
        fetch_web_source(
            url="https://example.com/retry",
            title="Retry Source",
            max_attempts=0,
        )


def test_fetch_web_source_rejects_negative_retry_delay() -> None:
    with pytest.raises(
        ValueError,
        match="retry_delay_seconds cannot be negative",
    ):
        fetch_web_source(
            url="https://example.com/retry",
            title="Retry Source",
            retry_delay_seconds=-0.1,
        )


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


def test_extract_text_from_html_ignores_style_and_script() -> None:
    html = (
        "<html>"
        "<head>"
        "<style>body { background: red; }</style>"
        "<script>console.log('ignore me')</script>"
        "</head>"
        "<body>"
        "<h1>Example Domain</h1>"
        "<p>Readable content</p>"
        "</body>"
        "</html>"
    )

    result = extract_text_from_html(html)

    assert result == "Example Domain Readable content"
    assert "background" not in result
    assert "console.log" not in result