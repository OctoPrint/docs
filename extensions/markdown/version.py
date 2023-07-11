from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension
import xml.etree.ElementTree as etree

VERSION_RE = r"\[{2}\s*version_(added|changed)\s+(.*)\s*\]{2}"


class VersionPattern(Pattern):
    def handleMatch(self, m):
        version = m.group(3).strip()

        link = etree.Element("a")
        link.set(
            "href",
            f"https://github.com/OctoPrint/OctoPrint/releases/tag/{m.group(3).strip()}",
        )
        link.text = version

        em = etree.Element("em")
        em.text = f"{m.group(2).capitalize()} in version "
        em.append(link)

        return em


class VersionExtension(Extension):
    def extendMarkdown(self, md):
        pattern = VersionPattern(VERSION_RE)
        md.inlinePatterns.register(
            pattern, "version", 20
        )  # 20 is priority, not sure what it should be


def makeExtension(**kwargs):
    return VersionExtension(**kwargs)
