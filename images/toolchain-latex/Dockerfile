FROM ghcr.io/roswellcityuk/dev-toolchains/base-tex:latest

# Install System Tools for LaTeX Workflows
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre-headless \
    ghostscript \
    hunspell \
    hunspell-en-us \
    libfile-homedir-perl \
    libyaml-tiny-perl \
    poppler-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Restore Global Configuration (latexmkrc)
RUN echo '$pdf_mode = 1;' > /usr/local/texlive/latexmkrc \
    && echo '$pdflatex = "pdflatex %O -interaction=nonstopmode -synctex=1 %S";' >> /usr/local/texlive/latexmkrc

# Verification & Metadata
RUN latexmk -v
LABEL org.opencontainers.image.source=https://github.com/roswellcityuk/dev-toolchains
LABEL org.opencontainers.image.description="LaTeX Toolchain (VS Code optimized)"