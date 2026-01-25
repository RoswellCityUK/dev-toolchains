# toolchain-amazon-publishing

Markdown-based publishing toolchain for publishing Books (eBook & Print).

## Features
- **Quarto**: For converting Markdown to multiple formats.
- **TeX Live**: For high-quality PDF (Print) generation.
- **Live Preview**: Real-time rendering via the Quarto VS Code extension.

## Suggested .devcontainer/devcontainer.json
```json
{
  "name": "KDP Publishing",
  "image": "ghcr.io/roswellcityuk/dev-toolchains/toolchain-amazon-publishing:latest",
  "customizations": {
    "vscode": {
      "extensions": ["quarto.quarto", "yzhang.markdown-all-in-one"],
      "settings": { "quarto.render.onSave": true }
    }
  },
  "remoteUser": "vscode"
}