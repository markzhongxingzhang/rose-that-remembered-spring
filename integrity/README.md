# Integrity record

Every public version of this record is registered here:

| item | what it is |
|---|---|
| version | the version identifier, for example `0.1.0`, with a matching git tag `v0.1.0` |
| prepared | the date the content of the version was prepared |
| released | the date the version was actually made public |
| commit | the git commit that the tag points to |
| manifest | the SHA-256 hash of every public file in that version (`integrity/v<version>/SHA256SUMS`) |
| manifest digest | the SHA-256 hash of the manifest file itself |
| signature | whether the release tag was cryptographically signed |
| third-party timestamp | whether an independent timestamp of the manifest was obtained, and where its proof is kept |

The record is in [RELEASES.md](RELEASES.md). The same record in machine-readable form is `releases.json`.

## What the manifest covers

The manifest covers every file in the repository except the integrity record itself:

- `integrity/RELEASES.md`
- `integrity/releases.json`
- `integrity/v*/SHA256SUMS`
- `integrity/v*/timestamp/*` (third-party timestamp proofs, where they exist)
- `docs/integrity.html`

These files record the manifest, so they cannot also be part of it. This is also why the commit of a version is recorded after the version is tagged.

## How to verify a version

```
git clone https://github.com/markzhongxingzhang/rose-that-remembered-spring.git
cd rose-that-remembered-spring
git checkout v0.1.0
sha256sum -c integrity/v0.1.0/SHA256SUMS
sha256sum integrity/v0.1.0/SHA256SUMS
git rev-parse "v0.1.0^{commit}"
```

The third command checks every listed file. Compare the output of the fourth with the manifest digest in [RELEASES.md](RELEASES.md), and the output of the fifth with the commit recorded there.

To check, in addition, that the version contains no files beyond those listed:

```
python3 tools/make_manifest.py --verify 0.1.0
```

## What this record does and does not show

- **It shows** that the files of a version are exactly the files listed in its manifest. Anyone can detect a later change.
- **The release date** is the date the version was first made public. The hosting service's own record of the tag and the release is the independent evidence for it.
- **Git commit dates** are set by whoever makes the commit. They are not independent evidence of time.
- **A third-party timestamp** is independent evidence that the manifest existed at the stamped time. This record lists one only where it was actually obtained, together with its proof file.
- **It does not show** who first had an idea.
