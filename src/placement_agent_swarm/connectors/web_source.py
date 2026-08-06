from html.parser import HTMLParser
from time import sleep
from urllib.error import URLError
from urllib.request import Request, urlopen

from placement_agent_swarm.config import WebSourceConfig
from placement_agent_swarm.schemas.source import CollectedSource

DEFAULT_WEB_SOURCE_CONFIG = WebSourceConfig()


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
    config: WebSourceConfig = DEFAULT_WEB_SOURCE_CONFIG,
) -> CollectedSource:
    request = Request(
        url,
        headers={
            "User-Agent": config.user_agent,
        },
    )

    last_error: URLError | TimeoutError | OSError | None = None

    for attempt in range(1, config.max_attempts + 1):
        try:
            with urlopen(
                request,
                timeout=config.request_timeout_seconds,
            ) as response:
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

            if attempt < config.max_attempts:
                sleep(config.retry_delay_seconds)

    raise WebSourceFetchError(
        f"Failed to fetch web source after "
        f"{config.max_attempts} attempts: {title}"
    ) from last_error