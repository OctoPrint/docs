import logging
import urllib.parse
import re

import mkdocs.plugins

log = logging.getLogger("mkdocs")

SITE_URLS_REGEX = re.compile(r'(href|src)="site:([^"]+)"', re.IGNORECASE)


@mkdocs.plugins.event_priority(50)
def on_page_content(html, page, config, files):
    site_url = config["site_url"]
    path = urllib.parse.urlparse(site_url).path

    if not path:
        path = "/"
    if not path.endswith("/"):
        path += "/"

    def _replace(match):
        param = match.group(1)
        url = match.group(2)
        if url.startswith("/"):
            url = url[1:]

        log.info(f"Replacing site:{match.group(2)} with {path}{url}...")
        return f'{param}="{path}{url}"'

    return SITE_URLS_REGEX.sub(_replace, html)
