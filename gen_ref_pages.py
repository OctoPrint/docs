"""Generate the code reference pages and navigation."""

from pathlib import Path
import os

import mkdocs_gen_files

SOURCE = os.environ.get("OCTOPRINT_SRC", "../OctoPrint/src")

ignore_str = os.environ.get("OCTOPRINT_SRC_IGNORE", "")
if ignore_str:
    IGNORE = ignore_str.split(",")
else:
    IGNORE = [
        "octoprint.plugins.",
        "octoprint.util.piptestballoon.",
        "octoprint._version",
    ]

nav = mkdocs_gen_files.Nav()

for path in sorted(Path(SOURCE).rglob("*.py")):
    module_path = path.relative_to(SOURCE).with_suffix("")
    doc_path = path.relative_to(SOURCE).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        if any(map(lambda i: ident.startswith(i), IGNORE)):
            continue
        fd.write(f"# {ident}\n")
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
