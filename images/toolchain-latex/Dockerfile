ARG BASE_IMAGE=ghcr.io/roswellcityuk/dev-toolchains/base-tex:latest
FROM ${BASE_IMAGE}

# Install System Tools for LaTeX Workflows
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
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