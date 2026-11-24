import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit
from urllib.request import urlopen

from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from mkdocs.structure.nav import get_navigation


SOURCE = "https://p3-llms.onrender.com/"
ORIGIN = urlsplit(SOURCE).netloc
CSS_URL = re.compile(r"""url\(\s*(['"]?)([^)'"\s]+)\1\s*\)""")
ROOT = Path(__file__).resolve().parents[1]


class ArticleResources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.has_article = False
        self.main_position = None
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "article":
            self.has_article = True
        if tag == "main" and self.main_position is None:
            self.main_position = self.getpos()
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


def add_site_header(page, main_position):
    config = load_config(config_file=str(ROOT / "mkdocs.yml"))
    nav = get_navigation(get_files(config), config)
    templates = config.theme.get_env()
    header = templates.get_template("site-header.html").render(
        config=config, nav=nav, page=None, base_url="/", mirrored=True
    )
    stylesheet = "/stylesheets/site-header.css"
    if config.extra["asset_version"]:
        stylesheet += f'?v={quote(config.extra["asset_version"], safe="")}'
    tracker = templates.get_template("analytics.html").render()

    line_number, column = main_position
    lines = page.split("\n")
    line = lines[line_number - 1]
    lines[line_number - 1] = f"{line[:column]}{header}\n{line[column:]}"
    head = f'<link rel="stylesheet" href="{stylesheet}">\n{tracker}\n</head>'
    return "\n".join(lines).replace("</head>", head, 1)


def mirror(destination):
    page = fetch(SOURCE).decode("utf-8")
    resources = ArticleResources()
    resources.feed(page)
    if not resources.has_article:
        raise ValueError("The public Argon page did not contain an article.")
    if resources.main_position is None:
        raise ValueError("The public Argon page did not contain a main element.")
    if "</head>" not in page:
        raise ValueError("The public Argon page did not have a closing head tag.")

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
    page = add_site_header(page, resources.main_position)
    (destination / "index.html").write_text(page, encoding="utf-8")
    print(f"Mirrored the public Argon article and {len(downloaded)} assets.")


if __name__ == "__main__":
    mirror(Path(sys.argv[1]))
