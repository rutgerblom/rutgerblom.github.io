"""Check that local image URLs in the generated HTML point to files."""

import re
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

CSS_URL = re.compile(r"""url\(\s*(?:'([^']*)'|"([^"]*)"|([^\s)]*))\s*\)""", re.I)


class ImageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img" and attrs.get("src"):
            self.urls.add(attrs["src"])
        if tag in {"img", "source"} and attrs.get("srcset"):
            for candidate in attrs["srcset"].split(","):
                fields = candidate.split()
                if fields:
                    self.urls.add(fields[0])
        for match in CSS_URL.finditer(attrs.get("style") or ""):
            self.urls.add(next(group for group in match.groups() if group is not None))


def main():
    output = Path(sys.argv[1]).resolve()
    config = Path("config/_default/config.toml")
    origin = tomllib.loads(config.read_text(encoding="utf-8"))["baseURL"]
    host = urlsplit(origin).netloc
    if not (output / "index.html").is_file():
        sys.exit(f"No built homepage in {output}")

    missing = []
    checked = set()
    for page in sorted(output.rglob("*.html")):
        relative_page = page.relative_to(output).as_posix()
        parser = ImageLinks()
        parser.feed(page.read_text(encoding="utf-8"))
        for url in sorted(parser.urls):
            resolved = urlsplit(urljoin(urljoin(origin, relative_page), url))
            if resolved.scheme not in {"http", "https"} or resolved.netloc != host:
                continue
            target = (output / unquote(resolved.path).lstrip("/")).resolve()
            if not target.is_relative_to(output) or not target.is_file():
                missing.append(f"{relative_page}: {url}")
            checked.add(target)

    if missing:
        sys.exit("Missing local images:\n" + "\n".join(missing))
    if not checked:
        sys.exit("No local images found in the built site")
    print(f"Verified {len(checked)} local images")


if __name__ == "__main__":
    main()
