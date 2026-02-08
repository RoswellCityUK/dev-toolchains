# Toolchain: Quarto Publishing

A comprehensive publishing toolchain designed for **Amazon KDP (Print & eBook)** and technical documentation. It combines the ease of Markdown with the power of TeX Live 2025 for PDF generation.

## ✨ Features
* **Core:** Quarto CLI (Latest Stable).
* **PDF Engine:** TeX Live 2025 (via `toolchain-latex` base).
* **Graphics:** `librsvg2` for SVG rendering in PDFs.
* **Syntax:** `python3-pygments` for code block highlighting.
* **Arch:** Native support for Intel (AMD64).

## 🛠 Usage: .devcontainer/devcontainer.json

Use this configuration for a seamless writing experience with **Live Preview**.

```json
{
  "name": "Quarto Book",
  "image": "ghcr.io/roswellcityuk/dev-toolchains/toolchain-quarto:latest",
  "customizations": {
    "vscode": {
      "extensions": [
        "quarto.quarto",
        "yzhang.markdown-all-in-one",
        "streetsidesoftware.code-spell-checker",
        "valentjn.vscode-ltex",
        "davidanson.vscode-markdownlint"
      ],
      "settings": {
        "quarto.render.onSave": true,
        "editor.wordWrap": "on",
        "ltex.language": "en-US",
        "ltex.java.path": "/usr/bin/java"
      }
    }
  },
  "remoteUser": "vscode"
}
```

## 📖 How to Build
To generate a PDF book (Print ready):
```bash
quarto render my-book --to pdf
```

To generate an ePub (Kindle ready):
```bash
quarto render my-book --to epub
```