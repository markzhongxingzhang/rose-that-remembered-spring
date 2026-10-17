#!/usr/bin/env python3
"""Build the static website in docs/ from the Markdown documents of this repository.

Standard library only. The output is deterministic: the same sources always give the same bytes.

    python3 tools/build_site.py            # write docs/
    python3 tools/build_site.py --out DIR  # write elsewhere (used to check that docs/ is current)
"""
import argparse
import html
import os
import posixpath
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (output file, nav label, page key, title, description, sources)
PAGES = [
    ("index.html", "Home", "home", "The Rose That Remembered Spring",
     "A literary-scientific research record on whether an artificial agent's past can change what it later does.",
     ["site/home.html"]),
    ("vision.html", "Vision", "vision", "Research Vision · The Rose That Remembered Spring",
     "The original question, the Canon Rule, the manifesto and what the project does not claim.",
     ["RESEARCH_VISION.md"]),
    ("timeline.html", "Timeline", "timeline", "Research Timeline · The Rose That Remembered Spring",
     "The phases of the research, dated, with how each one closed.",
     ["RESEARCH_TIMELINE.md"]),
    ("findings.html", "Findings", "findings", "Preliminary Findings · The Rose That Remembered Spring",
     "Bounded development-stage findings with status labels, failed instruments and open questions.",
     ["PRELIMINARY_FINDINGS.md"]),
    ("integrity.html", "Integrity", "integrity", "Integrity Record · The Rose That Remembered Spring",
     "Release record, SHA-256 manifest and how to verify a version.",
     ["integrity/RELEASES.md", "integrity/README.md"]),
    ("about.html", "About", "about", "About · The Rose That Remembered Spring",
     "Attribution, what this repository leaves out, and the rights notice.",
     ["ATTRIBUTION.md", "DISCLOSURE.md", "LICENSE.md"]),
    ("changelog.html", None, "changelog", "Changelog · The Rose That Remembered Spring",
     "Versions of this public record.",
     ["CHANGELOG.md"]),
]

# Where a repository path is published on the site.
LINK_MAP = {
    "README.md": "index.html",
    "RESEARCH_VISION.md": "vision.html",
    "RESEARCH_TIMELINE.md": "timeline.html",
    "PRELIMINARY_FINDINGS.md": "findings.html",
    "CHANGELOG.md": "changelog.html",
    "ATTRIBUTION.md": "about.html#attribution",
    "DISCLOSURE.md": "about.html#disclosure",
    "LICENSE.md": "about.html#license",
    "integrity/RELEASES.md": "integrity.html",
    "integrity/README.md": "integrity.html#verify",
    "integrity": "integrity.html",
    "docs": "index.html",
}

# Part ids on pages built from several documents.
PART_IDS = {"ATTRIBUTION.md": "attribution", "DISCLOSURE.md": "disclosure", "LICENSE.md": "license",
            "integrity/RELEASES.md": "releases", "integrity/README.md": "verify"}

# Page headings for pages assembled from several documents (their own headings move down one level).
PAGE_H1 = {"integrity": "Integrity", "about": "About this record"}

STATUS = {
    "REGISTERED · MET": "met",
    "REGISTERED · NOT MET": "notmet",
    "VALIDITY · PASSED": "passed",
    "VALIDITY · FAILED": "failed",
    "EXPLORATORY": "exploratory",
    "NOT TESTED": "nottested",
}

ITEM_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def slugify(text, used):
    s = re.sub(r"<[^>]+>", "", text)
    s = html.unescape(s).lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s.strip())
    s = s or "section"
    base, n = s, 2
    while s in used:
        s = f"{base}-{n}"
        n += 1
    used.add(s)
    return s


class Renderer:
    def __init__(self, source_rel, shift=0, used_ids=None):
        self.src_dir = posixpath.dirname(source_rel)
        self.shift = shift
        self.used_ids = used_ids if used_ids is not None else set()

    # inline ------------------------------------------------------------
    def rewrite(self, url):
        if re.match(r"^[a-z]+:", url) or url.startswith("#"):
            return url
        path, _, frag = url.partition("#")
        target = posixpath.normpath(posixpath.join(self.src_dir, path)).rstrip("/")
        if target in LINK_MAP:
            mapped = LINK_MAP[target]
            if frag and "#" not in mapped:
                mapped += "#" + frag
            return mapped
        raise SystemExit(f"build_site: link to {url!r} (resolved {target!r}) has no page on the site")

    def inline(self, text):
        out = []
        for part in re.split(r"(`[^`]+`)", text):
            if part.startswith("`") and part.endswith("`") and len(part) > 1:
                code = part[1:-1]
                if code in STATUS:
                    out.append(f'<span class="status status-{STATUS[code]}">{html.escape(code)}</span>')
                else:
                    out.append(f"<code>{html.escape(code)}</code>")
                continue
            t = html.escape(part, quote=False)
            t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                       lambda m: f'<a href="{html.escape(self.rewrite(html.unescape(m.group(2))))}">{m.group(1)}</a>', t)
            t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
            t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)
            t = re.sub(r"\{\{([A-Z_]+)\}\}", r'<mark class="owner-field">\1</mark>', t)
            out.append(t)
        return "".join(out)

    def para_inline(self, lines):
        parts = []
        for i, line in enumerate(lines):
            hard = line.endswith("\\")
            text = line[:-1] if hard else line
            parts.append(self.inline(text.strip()))
            if i < len(lines) - 1:
                parts.append("<br>\n" if hard else "\n")
        return "".join(parts)

    # blocks ------------------------------------------------------------
    @staticmethod
    def starts_block(line):
        return (line.startswith("#") or line.startswith(">") or line.startswith("```")
                or line.lstrip().startswith("|") or ITEM_RE.match(line) is not None
                or re.match(r"^\s*(-{3,}|\*{3,})\s*$", line) is not None)

    def blocks(self, lines):
        out = []
        i, n = 0, len(lines)
        while i < n:
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            if line.startswith("```"):
                j, buf = i + 1, []
                while j < n and not lines[j].startswith("```"):
                    buf.append(lines[j])
                    j += 1
                out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
                i = j + 1
                continue
            m = re.match(r"^(#{1,6})\s+(.*)$", line)
            if m:
                level, content = min(6, len(m.group(1)) + self.shift), self.inline(m.group(2).strip())
                hid = slugify(content, self.used_ids)
                out.append(f'<h{level} id="{hid}">{content}</h{level}>')
                i += 1
                continue
            if re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
                out.append("<hr>")
                i += 1
                continue
            if line.startswith(">"):
                buf = []
                while i < n and lines[i].startswith(">"):
                    buf.append(re.sub(r"^> ?", "", lines[i]))
                    i += 1
                out.append("<blockquote>\n" + self.blocks(buf) + "\n</blockquote>")
                continue
            if line.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
                rows = []
                while i < n and lines[i].lstrip().startswith("|"):
                    rows.append(lines[i])
                    i += 1
                out.append(self.table(rows))
                continue
            if ITEM_RE.match(line):
                html_list, i = self.list_block(lines, i)
                out.append(html_list)
                continue
            buf = []
            while i < n and lines[i].strip() and not (buf and self.starts_block(lines[i])):
                buf.append(lines[i])
                i += 1
            out.append("<p>" + self.para_inline(buf) + "</p>")
        return "\n".join(out)

    def table(self, rows):
        def cells(row):
            row = row.strip()
            if row.startswith("|"):
                row = row[1:]
            if row.endswith("|"):
                row = row[:-1]
            return [c.strip() for c in row.split("|")]
        head = cells(rows[0])
        body = [cells(r) for r in rows[2:]]
        h = "".join(f"<th>{self.inline(c)}</th>" for c in head)
        b = "\n".join("<tr>" + "".join(f"<td>{self.inline(c)}</td>" for c in r) + "</tr>" for r in body)
        return f'<div class="table-wrap"><table>\n<thead><tr>{h}</tr></thead>\n<tbody>\n{b}\n</tbody>\n</table></div>'

    def list_block(self, lines, i):
        m = ITEM_RE.match(lines[i])
        indent = len(m.group(1))
        ordered = m.group(2)[0].isdigit()
        items = []
        n = len(lines)
        while i < n:
            m = ITEM_RE.match(lines[i])
            if not m or len(m.group(1)) != indent or m.group(2)[0].isdigit() != ordered:
                break
            body = [m.group(3)]
            i += 1
            while i < n and lines[i].strip():
                mm = ITEM_RE.match(lines[i])
                if mm and len(mm.group(1)) <= indent:
                    break
                lead = len(lines[i]) - len(lines[i].lstrip())
                if lead <= indent and not mm:
                    break
                body.append(lines[i][min(lead, indent + 2):] if not mm else lines[i][indent + 2:])
                i += 1
            items.append(body)
        tag = "ol" if ordered else "ul"
        parts = []
        for body in items:
            first, rest = [body[0]], []
            for k, line in enumerate(body[1:], 1):
                if ITEM_RE.match(line):
                    rest = body[k:]
                    break
                first.append(line)
            inner = self.para_inline(first)
            if rest:
                inner += "\n" + self.blocks(rest)
            parts.append(f"<li>{inner}</li>")
        return f"<{tag}>\n" + "\n".join(parts) + f"\n</{tag}>", i


def nav_html(current):
    items = []
    for out, label, key, *_ in PAGES:
        if not label:
            continue
        cur = ' aria-current="page"' if key == current else ""
        items.append(f'<li><a href="{out}"{cur}>{label}</a></li>')
    return "\n".join(items)


def build(out_dir):
    template = read("site/templates/page.html")
    rose = read("site/assets/rose-inline.svg").strip()
    version = read("VERSION").strip()
    os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)
    for out, label, key, title, desc, sources in PAGES:
        if sources[0].endswith(".html"):
            content = read(sources[0]).strip()
            content = content.replace("%%ROSE_HERO%%", rose.replace("<svg ", '<svg class="hero-rose" ', 1))
            content = content.replace("%%VERSION%%", version)
        elif len(sources) == 1:
            content = Renderer(sources[0]).blocks(read(sources[0]).split("\n"))
        else:
            used = {"page-title"}
            chunks = [f'<h1 id="page-title">{html.escape(PAGE_H1[key])}</h1>']
            for src in sources:
                body = Renderer(src, shift=1, used_ids=used).blocks(read(src).split("\n"))
                chunks.append(f'<section class="about-part" id="{PART_IDS[src]}">\n{body}\n</section>')
            content = "\n".join(chunks)
        page = (template.replace("%%TITLE%%", html.escape(title))
                .replace("%%DESCRIPTION%%", html.escape(desc))
                .replace("%%KEY%%", key)
                .replace("%%ROSE%%", rose)
                .replace("%%NAV%%", nav_html(key))
                .replace("%%VERSION%%", version)
                .replace("%%CONTENT%%", content))
        with open(os.path.join(out_dir, out), "w", encoding="utf-8", newline="\n") as f:
            f.write(page)
    notfound = (template.replace("%%TITLE%%", "Not found · The Rose That Remembered Spring")
                .replace("%%DESCRIPTION%%", "Page not found.")
                .replace("%%KEY%%", "notfound").replace("%%ROSE%%", rose)
                .replace("%%NAV%%", nav_html(None)).replace("%%VERSION%%", version)
                .replace("%%CONTENT%%", '<h1>Not found</h1>\n<p>This page does not exist. '
                         'Return to the <a href="index.html">beginning</a>.</p>'))
    with open(os.path.join(out_dir, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(notfound)
    for name in ("site.css", "rose.svg"):
        shutil.copyfile(os.path.join(ROOT, "site/assets", name), os.path.join(out_dir, "assets", name))
    with open(os.path.join(out_dir, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "docs"))
    args = ap.parse_args()
    build(args.out)
    print(f"built {len(PAGES) + 1} pages into {os.path.relpath(args.out, ROOT) if args.out.startswith(ROOT) else args.out}")


if __name__ == "__main__":
    sys.exit(main())
