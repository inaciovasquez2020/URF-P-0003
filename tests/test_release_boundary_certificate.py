from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from release_boundary_certificate import missing_required_paths, release_boundary_certificate


BOUNDARY = """
No repository-level claim of peer-reviewed acceptance.
No repository-level claim of theorem-level completion beyond the listed certificate surface.
No repository-level claim of external validation.
"""


def test_missing_required_paths_detects_absence() -> None:
    missing = missing_required_paths(ROOT, ["docs/status/RELEASE_BOUNDARY_CERTIFICATE.md", "definitely_missing.file"])
    assert "definitely_missing.file" in missing


def test_release_boundary_certificate_passes_for_manifest() -> None:
    cert = release_boundary_certificate(
        ROOT,
        [
            "docs/status/RELEASE_BOUNDARY_CERTIFICATE.md",
            "scripts/verify_release_boundary_certificate.py",
            "src/release_boundary_certificate.py",
            "tests/test_release_boundary_certificate.py",
        ],
        BOUNDARY,
    )
    assert cert.theorem_id == "URFP0003-RBC-1"
    assert cert.status == "PASS"
    assert cert.required_count == 4
    assert cert.present_count == 4
    assert cert.missing == ()
    assert cert.all_required_present is True
    assert cert.nonclaim_boundary_declared is True


def test_release_boundary_certificate_fails_without_boundary() -> None:
    cert = release_boundary_certificate(ROOT, ["docs/status/RELEASE_BOUNDARY_CERTIFICATE.md"], "")
    assert cert.status == "FAIL"
    assert cert.nonclaim_boundary_declared is False


def test_repository_scope_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/verify_release_boundary_certificate.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert '"theorem_id": "URFP0003-RBC-1"' in result.stdout
    assert '"status": "PASS"' in result.stdout


def test_nonclaim_boundary_retained() -> None:
    text = (ROOT / "docs/status/RELEASE_BOUNDARY_CERTIFICATE.md").read_text(encoding="utf-8")
    assert "No repository-level claim of peer-reviewed acceptance." in text
    assert "No repository-level claim of theorem-level completion beyond the listed certificate surface." in text
    assert "No repository-level claim of external validation." in text
