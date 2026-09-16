import hashlib
from collections import defaultdict
from pathlib import Path


def _hash(path: Path, chunk: int = 65536) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while data := f.read(chunk):
            h.update(data)
    return h.hexdigest()


def find(roots: list[Path], min_size: int = 1) -> dict[str, list[Path]]:
    by_size: dict[int, list[Path]] = defaultdict(list)

    for root in roots:
        targets = [root] if root.is_file() else root.rglob("*")
        for p in targets:
            if not p.is_file():
                continue
            try:
                sz = p.stat().st_size
                if sz >= min_size:
                    by_size[sz].append(p)
            except OSError:
                pass

    by_hash: dict[str, list[Path]] = defaultdict(list)
    for files in by_size.values():
        if len(files) < 2:
            continue
        for f in files:
            try:
                by_hash[_hash(f)].append(f)
            except OSError:
                pass

    return {h: fs for h, fs in by_hash.items() if len(fs) > 1}
