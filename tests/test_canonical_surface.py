from pathlib import Path

def test_canonical_files_exist():
    for f in ["README.md", "STATUS.md", "FREEZE.md", "CITATION.cff", "manuscript.tex", "manuscript.pdf"]:
        assert Path(f).exists(), f

def test_no_tracked_latex_build_outputs():
    forbidden = [
        "manuscript.aux",
        "manuscript.fdb_latexmk",
        "manuscript.fls",
        "manuscript.log",
        "manuscript.out",
    ]
    for f in forbidden:
        assert not Path(f).exists(), f

def test_status_identity():
    txt = Path("STATUS.md").read_text()
    assert "URF-P-0003" in txt
