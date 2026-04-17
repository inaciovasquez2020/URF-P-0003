# FREEZE POLICY

## Canonical Surface

The following files define the repository claim boundary:

- README.md
- STATUS.md
- FREEZE.md
- CITATION.cff
- manuscript.tex
- manuscript.pdf

## Supporting Surface

The following are non-canonical support artifacts unless explicitly promoted:

- docs/
- infra/
- tex/
- workflows/
- generated logs
- local build outputs

## Mutation Policy

- `main` tracks canonical manuscript identity.
- No change may reintroduce transient LaTeX build artifacts into the canonical surface.
