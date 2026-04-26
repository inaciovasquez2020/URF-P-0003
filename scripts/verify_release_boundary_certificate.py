#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from release_boundary_certificate import release_boundary_certificate


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    doc = ROOT / "docs/status/RELEASE_BOUNDARY_CERTIFICATE.md"
    source = ROOT / "src/release_boundary_certificate.py"
    status = ROOT / "STATUS.md"
    if not status.exists():
        status = ROOT / "README.md"
    require(doc.exists(), "missing release boundary certificate doc")
    require(source.exists(), "missing certificate source")
    require(status.exists(), "missing status/readme boundary source")
    boundary_text = doc.read_text(encoding="utf-8") + "\n" + status.read_text(encoding="utf-8")
    cert = release_boundary_certificate(
        ROOT,
        [
            "docs/status/RELEASE_BOUNDARY_CERTIFICATE.md",
            "scripts/verify_release_boundary_certificate.py",
            "src/release_boundary_certificate.py",
            "tests/test_release_boundary_certificate.py",
        ],
        boundary_text,
    )
    require(cert.theorem_id == "URFP0003-RBC-1", "wrong theorem id")
    require(cert.status == "PASS", f"certificate failed: {cert}")
    require(cert.all_required_present, "required manifest is incomplete")
    require(cert.nonclaim_boundary_declared, "non-claim boundary missing")
    doc_text = doc.read_text(encoding="utf-8")
    for literal in [
        "Status: CLOSED repository-scope certificate.",
        "Theorem ID: URFP0003-RBC-1.",
        "No repository-level claim of peer-reviewed acceptance.",
        "No repository-level claim of theorem-level completion beyond the listed certificate surface.",
        "No repository-level claim of external validation.",
    ]:
        require(literal in doc_text, f"missing doc literal: {literal}")
    print(json.dumps(cert.__dict__, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
