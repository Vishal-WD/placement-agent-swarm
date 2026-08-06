from html.parser import HTMLParser
from time import sleep
from urllib.error import URLError
from urllib.request import Request, urlopen

from placement_agent_swarm.schemas.source import CollectedSource

DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_RETRY_DELAY_SECONDS = 1.0


class WebSourceFetchError(RuntimeError):
    """Raised when a web source cannot be fetched."""


class HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._ignored_tag_depth = 0

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        del attrs

        if tag in {"script", "style"}:
            self._ignored_tag_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._ignored_tag_depth > 0:
            self._ignored_tag_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._ignored_tag_depth > 0:
            return

        cleaned = data.strip()

        if cleaned:
            self._parts.append(cleaned)

    def get_text(self) -> str:
        return " ".join(self._parts)


def extract_text_from_html(html: str) -> str:
    parser = HTMLTextExtractor()
    parser.feed(html)
    return parser.get_text()


def fetch_web_source(
    *,
    url: str,
    title: str,
    source_type: str = "website",
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    retry_delay_seconds: float = DEFAULT_RETRY_DELAY_SECONDS,
) -> CollectedSource:
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    if retry_delay_seconds < 0:
        raise ValueError("retry_delay_seconds cannot be negative")

    request = Request(
        url,
        headers={
            "User-Agent": "placement-agent-swarm/0.1",
        },
    )

    last_error: URLError | TimeoutError | OSError | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            with urlopen(request, timeout=10) as response:
                html = response.read().decode(
                    "utf-8",
                    errors="replace",
                )

            content = extract_text_from_html(html)

            return CollectedSource.model_validate(
                {
                    "title": title,
                    "url": url,
                    "source_type": source_type,
                    "content": content,
                }
            )
        except (URLError, TimeoutError, OSError) as exc:
            last_error = exc

            if attempt < max_attempts:
                sleep(retry_delay_seconds)

    raise WebSourceFetchError(
        f"Failed to fetch web source after "
        f"{max_attempts} attempts: {title}"
    ) from last_error