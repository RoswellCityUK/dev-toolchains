# Stage 1: TeX Live for PDF rendering
FROM texlive/texlive:latest AS tex
RUN rm -rf /usr/local/texlive/*/texmf-dist/doc \
    && rm -rf /usr/local/texlive/*/texmf-dist/source

# Stage 2: Main Dev Container
FROM mcr.microsoft.com/devcontainers/base:bookworm

# Use ARG to capture the platform being built
ARG TARGETARCH

# 1. Install System Dependencies & Quarto
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    librsvg2-bin \
    python3-pygments \
    && if [ "$TARGETARCH" = "arm64" ]; then \
         QUARTO_URL="https://github.com/quarto-dev/quarto-cli/releases/download/v1.8.27/quarto-1.8.27-linux-arm64.deb"; \
       else \
         QUARTO_URL="https://github.com/quarto-dev/quarto-cli/releases/download/v1.8.27/quarto-1.8.27-linux-amd64.deb"; \
       fi \
    && curl -LO "$QUARTO_URL" \
    && dpkg -i "$(basename "$QUARTO_URL")" \
    && rm "$(basename "$QUARTO_URL")" \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Copy TeX Live from Stage 1 (needed for Print/PDF)
COPY --from=tex /usr/local/texlive /usr/local/texlive
RUN /usr/local/texlive/*/bin/*/tlmgr path add

USER vscode