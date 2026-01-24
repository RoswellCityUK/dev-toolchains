# toolchain-latex

LaTeX development toolchain image for VS Code Dev Containers.

## Includes
- TeX Live (Full distribution)
- `pandoc` (Markdown to PDF conversion)
- **Eisvogel** LaTeX template for professional Markdown-based PDFs
- `latexmk` & `biber`
- common TeX bundles: latex-extra, fonts, pictures, science
- `python3-pygments` (for minted workflows)
- `poppler-utils` / `ghostscript` (PDF utilities)

## ⚠️ Known Limitations
- **Documentation Removed:** To save ~3GB of space, the `texdoc` command and all TeX package documentation have been removed from this image. If you need to read package documentation, please use [CTAN](https://ctan.org) or `texdoc.org`.
- The vscode user has passwordless sudo access. To install missing TeX packages, use: `sudo tlmgr install <package_name>`

## Image
`ghcr.io/roswellcityuk/dev-toolchains/toolchain-latex`

## Suggested devcontainer.json
Copy this into your `.devcontainer/devcontainer.json` to enable automatic "Build on Save" for both LaTeX (`.tex`) and Markdown (`.md`) files.

```json
{
  "name": "latex",
  "image": "ghcr.io/roswellcityuk/dev-toolchains/toolchain-latex:latest",
  "customizations": {
    "vscode": {
      "extensions": ["james-yu.latex-workshop", "ban.spellright", "valentjn.vscode-ltex"],
      "settings": {
        "latex-workshop.latex.outDir": "%DIR%/../out",
        "latex-workshop.latex.autoBuild.run": "onSave",
        "latex-workshop.latex.recipes": [
          {
            "name": "latexmk",
            "tools": ["latexmk"]
          },
          {
            "name": "Markdown -> PDF (Pandoc + Eisvogel)",
            "tools": ["pandoc"]
          }
        ],
        "latex-workshop.latex.tools": [
          {
            "name": "latexmk",
            "command": "latexmk",
            "args": [
              "-synctex=1",
              "-interaction=nonstopmode",
              "-file-line-error",
              "-pdf",
              "-outdir=%DIR%/../out", 
              "-shell-escape",
              "%DOC%"
            ]
          },
          {
            "name": "pandoc",
            "command": "pandoc",
            "args": [
              "%DOC%.md",
              "-o",
              "%DIR%/../out/%DOCFILE%.pdf",
              "--from=markdown",
              "--template=eisvogel",
              "--listings",
              "--pdf-engine=pdflatex"
            ]
          }
        ]
      }
    }
  },
  "remoteUser": "vscode"
}

## Preview

![Preview of the workspace v0.0.4](./docs/preview.png)
