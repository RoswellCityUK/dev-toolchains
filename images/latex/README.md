# toolchain-latex

LaTeX development toolchain image for VS Code Dev Containers.

## Includes
- TeX Live (Debian packages)
- `latexmk`
- `biber` + bibtex extras
- common TeX bundles: latex-extra, fonts, pictures, science
- `python3-pygments` (for minted workflows)
- `poppler-utils` / `ghostscript` (PDF utilities)

## Image
`ghcr.io/roswellcityuk/toolchain-latex`

## Tags
- `texlive-2024.X.Y`
- `texlive-2024`
- `latest`

## Suggested devcontainer.json
```json
{
  "name": "latex",
  "image": "ghcr.io/roswellcityuk/toolchain-latex:texlive-2024",
  "customizations": {
    "vscode": {
      "extensions": ["james-yu.latex-workshop"],
      "settings": {
        "latex-workshop.latex.autoBuild.run": "onSave",
        "latex-workshop.latex.outDir": "%DIR%/out",
        "latex-workshop.view.pdf.viewer": "tab"
      }
    }
  },
  "remoteUser": "vscode"
}
