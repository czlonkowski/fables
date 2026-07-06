#!/usr/bin/env python3
"""Upload changed documents from a local export folder to the ingestion API."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import urllib.request

STATE_FILE = ".sync_state.json"


def load_state(source: Path) -> dict:
    state_path = source / STATE_FILE
    if state_path.exists():
        return json.loads(state_path.read_text())
    return {}


def save_state(source: Path, state: dict) -> None:
    (source / STATE_FILE).write_text(json.dumps(state, indent=2))


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_changed(source: Path, state: dict) -> list[Path]:
    changed = []
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.name == STATE_FILE:
            continue
        if path.suffix.lower() not in (".pdf", ".docx", ".txt"):
            continue
        digest = file_digest(path)
        if state.get(str(path.relative_to(source))) != digest:
            changed.append(path)
    return changed


def upload(api_url: str, api_key: str, path: Path, source: Path) -> None:
    payload = {
        "filename": str(path.relative_to(source)),
        "content_b64": None,  # streamed separately in v2; inline for now
    }
    import base64

    payload["content_b64"] = base64.b64encode(path.read_bytes()).decode()
    req = urllib.request.Request(
        f"{api_url.rstrip('/')}/documents",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        if resp.status >= 300:
            raise RuntimeError(f"upload failed for {path}: HTTP {resp.status}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="export folder to scan")
    parser.add_argument("--api-url", required=True, help="ingestion API base URL")
    parser.add_argument("--api-key", required=True, help="ingestion API key")
    args = parser.parse_args()

    state = load_state(args.source)
    changed = collect_changed(args.source, state)
    print(f"{len(changed)} changed file(s)")

    for path in changed:
        upload(args.api_url, args.api_key, path, args.source)
        state[str(path.relative_to(args.source))] = file_digest(path)
        print(f"uploaded {path}")

    save_state(args.source, state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
