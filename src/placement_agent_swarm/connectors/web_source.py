from html.parser import HTMLParser
from urllib.request import Request, urlopen

from placement_agent_swarm.schemas.source import CollectedSource


class HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
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
) -> CollectedSource:
    request = Request(
        url,
        headers={
            "User-Agent": "placement-agent-swarm/0.1",
        },
    )

    with urlopen(request, timeout=10) as response:
        html = response.read().decode("utf-8", errors="replace")

    content = extract_text_from_html(html)

    return CollectedSource.model_validate(
        {
            "title": title,
            "url": url,
            "source_type": source_type,
            "content": content,
        }
    )