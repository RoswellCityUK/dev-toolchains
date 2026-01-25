# Toolchain: LaTeX

A specialized Development Container for writing academic papers and documents in VS Code. It is built on top of a highly optimized **TeX Live 2025** distribution.

## ✨ Features
* **Base:** TeX Live 2025 (Scheme Full, minus documentation).
* **Engine:** `latexmk`, `biber`, `pdflatex`, `lualatex`, `xelatex`.
* **Utilities:**
    * `ghostscript` & `poppler-utils` (for PDF processing).
    * `python3-pygments` (for `minted` code highlighting).
    * `hunspell` (for spell checking).
    * `make` & `git` (for CI/CD workflows).
* **Configuration:** Pre-configured `latexmkrc` for "out-of-the-box" builds.

## ⚠️ Limitations
* **No Documentation:** To save ~3GB of space, `texdoc` and manual pages are removed. Use [CTAN.org](https://ctan.org) for reference.
* **Rootless:** Runs as user `vscode` by default (with sudo access).

## 🛠 Usage: .devcontainer/devcontainer.json

Copy the configuration below to set up your project. It configures the **LaTeX Workshop** extension to build automatically on save.

```json
{
  "name": "LaTeX Project",
  "image": "ghcr.io/roswellcityuk/dev-toolchains/toolchain-latex:latest",
  "customizations": {
    "vscode": {
      "extensions": [
        "james-yu.latex-workshop",
        "ban.spellright",
        "valentjn.vscode-ltex"
      ],
      "settings": {
        "latex-workshop.latex.outDir": "%DIR%/../out",
        "latex-workshop.latex.autoBuild.run": "onSave",
        "latex-workshop.latex.recipes": [
          {
            "name": "latexmk (pdf)",
            "tools": ["latexmk"]
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
          }
        ]
      }
    }
  },
  "remoteUser": "vscode"
}
```

## Manual Package Installation
If you need a package that was somehow excluded:
```bash
sudo tlmgr install <package_name>
```