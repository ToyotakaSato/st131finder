# Source and deterministic build

This directory contains everything needed to rebuild the released ST131Finder
file byte for byte.

| File | Description |
|---|---|
| `app.html` | The source template: the complete application with four placeholders (`__DBZ_BASE64__`, `__VER__`, `__BUILT__`, `__ALGO__`, `__DB__`) that the builder fills in |
| `db.json` | The reference database: PubMLST *Escherichia coli* #1 (Achtman) scheme, ResFinder, and the ECTyper O- and H-antigen allele set, all retrieved August 2026 |
| `build_release.py` | The deterministic release builder |

## Rebuilding

Python 3.9 or later, no third-party packages:

```bash
cd src
python3 build_release.py
```

This writes `st131finder-v1.3.0.html` and prints the three digests.

## Verifying the published release

```bash
cd src
python3 build_release.py --check ../st131finder-v1.3.0.html
```

Expected output:

```
release file  97114e1c8e6b9b7106a8f9699125ea0bcbf93e073f3e2f2478953a57b3a52ab0
algorithm     c775cb3c1f9b275e5b89bd4d8bc5c2d883decb84cd9af4ce34c9e6b8fa5cf76d
db.json       89e9166a635090c044669978cc47568d73595e044e403542b7ceb9a6f3f2479a

OK: rebuild is byte-identical to ../st131finder-v1.3.0.html
```

These are the digests reported in the accompanying paper.

## How determinism is achieved

A gzip stream ordinarily records the modification time of the input and the
operating system of the machine that produced it, so the same input compressed
on two machines yields two different files. The builder pins both: the
modification timestamp is set to zero and the OS byte to `0xFF` ("unknown").
Compression level is fixed at 9. The result is that `db.json` always encodes to
the same 926,627 bytes regardless of when or where the build runs.

The algorithm digest covers the release script from the assay-definition marker
to the end of that script. The version block — which carries the digests
themselves — sits above that marker, so stamping the version can never perturb
the region being hashed. The digest is in any case computed before stamping.

## Reference data

`db.json` is provided directly rather than as a download script. The upstream
databases are living resources that change without notice, so a script that
re-fetched them would not reproduce the build that generated the results in the
paper. The copy here is the exact database used, and its SHA-256 digest is
published with the release.

Source databases and their retrieval dates:

- PubMLST *Escherichia coli* #1 (Achtman) scheme — August 2026
- ResFinder — August 2026
- ECTyper O- and H-antigen allele set — August 2026
- O25b: *pabB* PCR of Clermont et al. 2008, *J Antimicrob Chemother* 61:1024

Each is redistributable under its own terms; check the current terms before
redistributing a rebuilt database.
