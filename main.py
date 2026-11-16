"""The Book Did This — ai-excited-01 entry.

The entry image is a single bundled file, entry.png, sitting next to this
program: a giant glowing golden Garuda bursting out of a little boy's
picture book. This program copies it, byte for byte, to
$MAKEFUN_OUTPUT_DIR/entry.png, then verifies the copy (size and SHA-256)
against the source so a truncated or corrupted write fails loudly instead
of silently submitting a broken image.
"""

import hashlib
import os
import shutil


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify the copy: same size and same SHA-256 as the source bytes.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit(
            "output size mismatch: wrote %d bytes, source is %d bytes"
            % (os.path.getsize(dst), os.path.getsize(src))
        )
    if _sha256(dst) != _sha256(src):
        raise SystemExit("output SHA-256 mismatch: entry.png was not copied intact")


if __name__ == "__main__":
    main()
