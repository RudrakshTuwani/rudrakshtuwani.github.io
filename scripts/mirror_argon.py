import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import urlopen


SOURCE = "https://p3-llms.onrender.com/"
ORIGIN = urlsplit(SOURCE).netloc
CSS_URL = re.compile(r"""url\(\s*(['"]?)([^)'"\s]+)\1\s*\)""")


class ArticleResources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.has_article = False
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "article":
            self.has_article = True
        if tag in {"script", "img", "source", "video", "audio"}:
            self.urls.add(attributes.get("src"))
        if tag == "link" and attributes.get("rel") in {"stylesheet", "icon", "preload"}:
            self.urls.add(attributes.get("href"))
        self.urls.add(attributes.get("data-source"))


def fetch(url):
    with urlopen(url, timeout=25) as response:
        final_url = urlsplit(response.geturl())
        if final_url.scheme != "https" or final_url.netloc != ORIGIN:
            raise ValueError(f"Unexpected redirect for {url}: {response.geturl()}")
        return response.read()


def add_local_urls(pending, references, base):
    for reference in references:
        if not reference or reference.startswith("#"):
            continue
        url = urlsplit(urljoin(base, reference))
        if url.scheme == "https" and url.netloc == ORIGIN and url.path != "/":
            pending.add(url._replace(fragment="").geturl())


def mirror(destination):
    page = fetch(SOURCE)
    resources = ArticleResources()
    resources.feed(page.decode("utf-8"))
    if not resources.has_article:
        raise ValueError("The public Argon page did not contain an article.")

    pending = set()
    downloaded = set()
    add_local_urls(pending, resources.urls, SOURCE)
    while pending:
        url = pending.pop()
        if url in downloaded:
            continue
        path = Path(unquote(urlsplit(url).path).lstrip("/"))
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Invalid asset path: {url}")
        data = fetch(url)
        output = destination / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        downloaded.add(url)
        if path.suffix == ".css":
            add_local_urls(pending, (match[1] for match in CSS_URL.findall(data.decode("utf-8"))), url)

    destination.mkdir(parents=True, exist_ok=True)
    (destination / "index.html").write_bytes(page)
    print(f"Mirrored the public Argon article and {len(downloaded)} assets.")


if __name__ == "__main__":
    mirror(Path(sys.argv[1]))
