# Toolchain: Quarto Publishing

A publishing environment designed for **Amazon KDP (Print & eBook)**, academic journals, and technical documentation.

This toolchain goes beyond basic Quarto installation. It includes an **Automated Publishing Pipeline** that enforces publisher standards (margins, gutters, cover requirements) and generates ready-to-upload artifacts.

## ✨ Key Capabilities

### 1. 🏭 Automated Scaffolding (`scaffold-project`)
Don't start from scratch. The built-in wizard sets up professional directory structures (`chapters/`, `assets/`) and configures `_quarto.yml` for specific publishers:
* **Amazon KDP:** Sets up Hybrid Output (ePub + PDF) and interactive margin configuration.
* **Academic Journals:** ACM, Elsevier, Springer, PLOS, ACS.
* **Generic Books:** Standard technical book structure.

### 2. ⚖️ Amazon KDP Logic Engine
Includes a dedicated logic library (`kdp_specs.py`) that:
* Validates **Ink/Paper/Trim Size** combinations against Amazon's manufacturing rules.
* Calculates required **Gutter Margins** based on your exact page count.
* Ensures PDF covers are removed (for Print) and ePub covers are present (for Kindle).

### 3. 🛡️ Quality Assurance (`check-project`)
A pre-flight linter that acts as your technical editor. It checks:
* **Structure:** Missing chapters, broken image links, missing bibliography.
* **Content:** Scans for leftover `TODO` or `FIXME` markers.
* **Physical Specs:** Verifies that your `_quarto.yml` geometry matches the physical page count of your output.

### 4. 📦 Release Automation (`build-release`)
One command to rule them all.
1.  Runs the **Linter**.
2.  **Cleans** previous builds.
3.  **Renders** all formats (PDF, ePub, HTML).
4.  **Validates** the final PDF page count.
5.  **Packages** everything into a versioned ZIP file (e.g., `release_20231027.zip`).

---

## 🚀 The Workflow

### Step 1: Initialize
Start a new book. The script will ask for your target publisher and (for KDP) your paper choice to calculate margins.

```bash
scaffold-project
```

### Step 2: Write & Preview
Use VS Code to write content. The environment supports **Live Preview**.
* **Edit:** `chapters/intro.qmd`
* **Preview:** Run `quarto preview` in the terminal.

### Step 3: Check Your Work
Before building, run the linter to catch errors.

```bash
check-project
```

### Step 4: Build & Release
Generate the final artifacts. This script generates a zip file containing your upload-ready `ebook.epub` and `paperback.pdf`.

```bash
build-release
```

---

## 🛠️ Usage: Devcontainer

To use this image in VS Code or GitHub Codespaces, use the following `.devcontainer/devcontainer.json`.

```json
{
  "name": "Quarto Publishing Engine",
  "image": "ghcr.io/roswellcityuk/dev-toolchains/toolchain-quarto:latest",
  "customizations": {
    "vscode": {
      "extensions": [
        "quarto.quarto",
        "yzhang.markdown-all-in-one",
        "streetsidesoftware.code-spell-checker",
        "valentjn.vscode-ltex",        // Grammar checking
        "redhat.vscode-yaml",          // For _quarto.yml validation
        "tamasfe.even-better-toml",     // For configuration files
        "davidanson.vscode-markdownlint"
      ],
      "settings": {
        "quarto.render.onSave": true,
        "editor.wordWrap": "on",
        "files.autoSave": "afterDelay",
        "ltex.language": "en-US",
        "ltex.java.path": "/usr/bin/java"
      }
    }
  },
  "remoteUser": "vscode"
}
```

---

## 🧩 Tech Stack

This image is built on a "batteries-included" philosophy:

| Component | Version | Description |
| :--- | :--- | :--- |
| **Quarto** | Latest | The core publishing CLI. |
| **TeX Live** | 2025 | Full TeX distribution for high-quality PDF generation. |
| **Python** | 3.x | Includes `jupyter`, `pandas`, `matplotlib`, `pypdf`. |
| **Rust** | Stable | Includes `evcxr` kernel for executable Rust code blocks. |
| **Go** | Latest | Includes `gonb` kernel for Go code blocks. |
| **.NET** | LTS | Includes C# and F# kernels via .NET Interactive. |
| **Tools** | Various | `graphviz`, `librsvg2`, `hunspell` (spellcheck). |

## 📚 KDP Margin Reference

The container automatically enforces these Amazon KDP standard margins:

| Page Count | Gutter (Inside Margin) |
| :--- | :--- |
| **24 - 150** | 0.375" |
| **151 - 300** | 0.500" |
| **301 - 500** | 0.625" |
| **501 - 700** | 0.750" |
| **701 - 828** | 0.875" |