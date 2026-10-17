#!/usr/bin/env python3
"""Write, record and verify the SHA-256 manifest of a public version.

    python3 tools/make_manifest.py 0.1.0 --prepared 2026-10-17
        write integrity/v0.1.0/SHA256SUMS, record its digest and the document hashes in
        integrity/releases.json and integrity/RELEASES.md, and rebuild docs/integrity.html

    python3 tools/make_manifest.py 0.1.0 --record-release --released 2026-10-20 --commit <full hash>
        [--signature "..."] [--timestamp "..."]
        record the actual release; touches only the integrity record (excluded from the manifest)

    python3 tools/make_manifest.py --verify 0.1.0
        check every listed file and report any file that is not listed

Standard library only.
"""
import argparse
import fnmatch
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

EXCLUDED = ["integrity/RELEASES.md", "integrity/releases.json", "integrity/v*/SHA256SUMS", "integrity/v*/timestamp/*",
            "docs/integrity.html"]
SKIP_DIRS = {".git", "__pycache__"}
DOCUMENTS = ["README.md", "RESEARCH_VISION.md", "RESEARCH_TIMELINE.md", "PRELIMINARY_FINDINGS.md", "CHANGELOG.md",
             "ATTRIBUTION.md", "DISCLOSURE.md", "LICENSE.md", "integrity/README.md"]
RELEASES_JSON = os.path.join(ROOT, "integrity", "releases.json")
RELEASES_MD = os.path.join(ROOT, "integrity", "RELEASES.md")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def public_files():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT).replace(os.sep, "/")
            if any(fnmatch.fnmatchcase(rel, pat) for pat in EXCLUDED):
                continue
            files.append(rel)
    return sorted(files)


def manifest_path(version):
    return os.path.join(ROOT, "integrity", f"v{version}", "SHA256SUMS")


def load_releases():
    if os.path.exists(RELEASES_JSON):
        with open(RELEASES_JSON, encoding="utf-8") as f:
            return json.load(f)
    return {"releases": []}


def save_releases(data):
    with open(RELEASES_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    render_releases_md(data)
    import build_site
    build_site.build(os.path.join(ROOT, "docs"))


def render_releases_md(data):
    lines = ["# Release record", "",
             "Each public version of this record, as it was actually released. "
             "How the manifest is made, and how to check it, is explained in [the integrity record](README.md).", "",
             "| version | prepared | released | commit | manifest digest (SHA-256) | signature | third-party timestamp |",
             "|---|---|---|---|---|---|---|"]
    for r in data["releases"]:
        lines.append("| {v} | {p} | {rel} | {c} | `{d}…` | {s} | {t} |".format(
            v=r["version"], p=r["prepared"], rel=r["released"] or "not yet released",
            c=f"`{r['commit'][:12]}…`" if r["commit"] else "not yet recorded",
            d=r["manifest_sha256"][:16], s=r["signature"], t=r["timestamp"]))
    for r in data["releases"]:
        lines += ["", f"## Version {r['version']}", "",
                  f"- **Tag:** `{r['tag']}`",
                  f"- **Content prepared:** {r['prepared']}",
                  f"- **Released:** {r['released'] or 'not yet released'}",
                  f"- **Commit:** {('`' + r['commit'] + '`') if r['commit'] else 'not yet recorded'}",
                  f"- **Manifest:** `{r['manifest']}`, {r['files']} files",
                  f"- **Manifest digest (SHA-256):** `{r['manifest_sha256']}`",
                  f"- **Signature:** {r['signature']}",
                  f"- **Third-party timestamp:** {r['timestamp']}",
                  "", "| document | SHA-256 |", "|---|---|"]
        for doc, digest in r["documents"].items():
            lines.append(f"| {doc} | `{digest}` |")
    with open(RELEASES_MD, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def write_manifest(version, prepared):
    import build_site
    if not os.path.exists(RELEASES_MD):
        render_releases_md(load_releases())
    build_site.build(os.path.join(ROOT, "docs"))
    files = public_files()
    out = manifest_path(version)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        for rel in files:
            f.write(f"{sha256(os.path.join(ROOT, rel))}  {rel}\n")
    digest = sha256(out)
    data = load_releases()
    entry = {"version": version, "tag": f"v{version}", "prepared": prepared, "released": None, "commit": None,
             "manifest": f"integrity/v{version}/SHA256SUMS", "manifest_sha256": digest, "files": len(files),
             "documents": {d: sha256(os.path.join(ROOT, d)) for d in DOCUMENTS},
             "signature": "none created", "timestamp": "none obtained"}
    data["releases"] = [r for r in data["releases"] if r["version"] != version] + [entry]
    data["releases"].sort(key=lambda r: [int(x) for x in r["version"].split(".")])
    save_releases(data)
    print(f"manifest {os.path.relpath(out, ROOT)}: {len(files)} files, sha256 {digest}")


def record_release(version, released, commit, signature, timestamp):
    data = load_releases()
    for r in data["releases"]:
        if r["version"] == version:
            if sha256(manifest_path(version)) != r["manifest_sha256"]:
                raise SystemExit("manifest on disk does not match the recorded digest")
            r["released"], r["commit"] = released, commit
            if signature:
                r["signature"] = signature
            if timestamp:
                r["timestamp"] = timestamp
            save_releases(data)
            print(f"recorded release {version}: {released}, commit {commit}")
            return
    raise SystemExit(f"version {version} is not in the record")


def verify(version):
    path = manifest_path(version)
    listed, bad = {}, 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            digest, rel = line.rstrip("\n").split("  ", 1)
            listed[rel] = digest
    for rel, digest in listed.items():
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            print(f"MISSING  {rel}")
            bad += 1
        elif sha256(full) != digest:
            print(f"CHANGED  {rel}")
            bad += 1
    for rel in public_files():
        if rel not in listed:
            print(f"EXTRA    {rel}")
            bad += 1
    print(f"{len(listed)} files listed; manifest sha256 {sha256(path)}; {'OK' if not bad else f'{bad} problem(s)'}")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("version", nargs="?")
    ap.add_argument("--prepared")
    ap.add_argument("--record-release", action="store_true")
    ap.add_argument("--released")
    ap.add_argument("--commit")
    ap.add_argument("--signature")
    ap.add_argument("--timestamp")
    ap.add_argument("--verify", metavar="VERSION")
    a = ap.parse_args()
    if a.verify:
        return verify(a.verify)
    if not a.version:
        ap.error("version required")
    if a.record_release:
        if not (a.released and a.commit and len(a.commit) == 40):
            ap.error("--released DATE and a full 40-character --commit are required")
        return record_release(a.version, a.released, a.commit, a.signature, a.timestamp)
    if not a.prepared:
        ap.error("--prepared DATE required")
    write_manifest(a.version, a.prepared)
    return 0


if __name__ == "__main__":
    sys.exit(main())
