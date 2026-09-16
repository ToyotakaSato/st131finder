#!/usr/bin/env python3
"""
Deterministic release builder for ST131Finder.

Assembles the single-file release from `app.html` (the source template) and
`db.json` (the reference database). The build is byte-for-byte reproducible:
running this script twice on the same inputs produces identical output, and
the SHA-256 digest of the released file can therefore be published alongside
the paper and re-derived by any reader.

Determinism is achieved by

  * pinning the gzip modification timestamp to zero,
  * pinning the gzip OS byte to 0xFF ("unknown") so the build does not carry
    the identity of the machine it was produced on, and
  * stamping the version block only after the algorithm digest is taken, so
    that stamping can never perturb the hashed region.

The algorithm digest covers the release script from the assay-definition
marker to the end of that script. The version block sits above the marker and
is therefore outside the digest by construction.

Usage:
    python3 build_release.py            # builds st131finder-v<VERSION>.html
    python3 build_release.py --check FILE
                                        # rebuilds and compares against FILE
"""

import argparse
import base64
import gzip
import hashlib
import pathlib
import sys

VERSION = "1.3.0"
BUILT = "2026-08-28"

HERE = pathlib.Path(__file__).resolve().parent
APP = HERE / "app.html"
DB = HERE / "db.json"

MARKER = "/* ============================ assay definitions ============================ */"
DBZ_OPEN = '<script id="dbz" type="application/octet-stream">'


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compress_db(db_bytes: bytes) -> bytes:
    """gzip with every source of nondeterminism pinned."""
    out = bytearray(gzip.compress(db_bytes, compresslevel=9, mtime=0))
    out[9] = 0xFF  # OS byte: "unknown" rather than the build host's OS
    return bytes(out)


def algorithm_region(html: str) -> str:
    """The hashed region: assay-definition marker to the end of that script."""
    start = html.index(MARKER)
    end = html.index("</script>", start)
    return html[start:end]


def build() -> tuple[str, dict]:
    app = APP.read_text(encoding="utf-8")
    db_bytes = DB.read_bytes()

    db_digest = sha256_bytes(db_bytes)
    payload = base64.b64encode(compress_db(db_bytes)).decode("ascii")

    html = app.replace("__DBZ_BASE64__", payload)

    # The algorithm digest is taken before the version block is stamped.
    algo_digest = sha256_bytes(algorithm_region(html).encode("utf-8"))

    html = (html
            .replace("__VER__", VERSION)
            .replace("__BUILT__", BUILT)
            .replace("__ALGO__", algo_digest)
            .replace("__DB__", db_digest))

    digests = {
        "release": sha256_bytes(html.encode("utf-8")),
        "algorithm": algo_digest,
        "db": db_digest,
    }
    return html, digests


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", metavar="FILE",
                    help="rebuild and compare byte for byte against FILE")
    ap.add_argument("-o", "--output", metavar="FILE",
                    help="write to FILE instead of st131finder-v<VERSION>.html")
    args = ap.parse_args()

    html, digests = build()
    data = html.encode("utf-8")

    print(f"release file  {digests['release']}")
    print(f"algorithm     {digests['algorithm']}")
    print(f"db.json       {digests['db']}")

    if args.check:
        reference = pathlib.Path(args.check).read_bytes()
        if reference == data:
            print(f"\nOK: rebuild is byte-identical to {args.check}")
            return 0
        print(f"\nMISMATCH: rebuild differs from {args.check}", file=sys.stderr)
        print(f"  rebuilt   {len(data)} bytes, sha256 {sha256_bytes(data)}", file=sys.stderr)
        print(f"  reference {len(reference)} bytes, sha256 {sha256_bytes(reference)}", file=sys.stderr)
        return 1

    out = pathlib.Path(args.output) if args.output else HERE / f"st131finder-v{VERSION}.html"
    out.write_bytes(data)
    print(f"\nwrote {out} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
