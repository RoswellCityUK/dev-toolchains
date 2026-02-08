# Dev Toolchains

A mono-repo of reusable Development Container images.

## 🏗 Architecture

This repository uses a **tiered build strategy** to maximize caching and minimize storage.

1.  **Platform (Base):** `base-tex`
    * **OS:** Debian Bookworm (via Microsoft DevContainers base)
    * **Core:** TeX Live 2025 (Custom Profile, No Docs, AMD64 Only)
    * **Common:** Git, Python (Pygments), Curl, Locales
2.  **Toolchains:**
    * `toolchain-latex`: Adds Build Tools (Make, Java), PDF Utils (Ghostscript), and VS Code helpers.
    * `toolchain-quarto`: Adds Quarto CLI and SVG rendering engines.

## 📦 Available Images

| Image | Tag | Description | Size (Est.) |
| :--- | :--- | :--- | :--- |
| **LaTeX** | `ghcr.io/roswellcityuk/dev-toolchains/toolchain-latex:latest` | Full TeX Live 2025 + VS Code Utilities | ~1.8 GB |
| **Quarto** | `ghcr.io/roswellcityuk/dev-toolchains/toolchain-quarto:latest` | Quarto CLI + TeX Live 2025 | ~1.9 GB |

## 🚀 Local Development

We use a `Makefile` to simplify local testing and building.

### Prerequisites
* Docker Desktop (running)
* Make

### Build Commands
```bash
# 1. Build the Base Image (Required first)
make base

# 2. Build all toolchains (Requires base)
make toolchains

# 3. Build a specific toolchain only
make build-local-latex
make build-local-quarto
```

*Note: Local builds use `--load` to make images available to your Docker daemon immediately.*

## 🤝 Contributing

1.  **Modify:** Edit the `Dockerfile` in `images/`.
2.  **Test:** Run `make build-local-<image>` and verify the output.
3.  **Push:** Create a PR. GitHub Actions will automatically:
    * Build the Base (if changed).
    * Build the Children (if Base changed or Child changed).
    * Publish to GHCR (on main merge).