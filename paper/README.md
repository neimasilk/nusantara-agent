# Paper Draft (LaTeX)

## Files
- `paper/main.tex`
- `paper/references.bib`

## Compile (from repo root)
```bash
pdflatex -output-directory=paper paper/main.tex
bibtex paper/main
pdflatex -output-directory=paper paper/main.tex
pdflatex -output-directory=paper paper/main.tex
```

## Draft policy
- Treat this as pilot-stage manuscript.
- Do not claim final generalization performance before held-out evaluation and dependency-complete reruns are finalized.
- Keep dev metrics and publication metrics separated.
