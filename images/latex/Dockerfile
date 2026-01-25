# Stage 1: Upstream TeX Live
FROM texlive/texlive:latest AS tex

# OPTIMIZATION: Remove docs and source code to save space
RUN rm -rf /usr/local/texlive/*/texmf-dist/doc \
    && rm -rf /usr/local/texlive/*/texmf-dist/source

# Stage 2: Your Dev Container
FROM mcr.microsoft.com/devcontainers/base:bookworm

LABEL org.opencontainers.image.source=https://github.com/roswellcityuk/dev-toolchains
LABEL org.opencontainers.image.description="LaTeX Dev Container"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    default-jre-headless \
    ghostscript \
    git \
    hunspell \
    hunspell-en-us \
    libfile-homedir-perl \
    libyaml-tiny-perl \
    locales \
    make \
    perl \
    poppler-utils \
    python3-pygments \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# 2. Copy TeX Live from Stage 1
COPY --from=tex /usr/local/texlive /usr/local/texlive

# 3. Link TeX Live to your PATH
RUN /usr/local/texlive/*/bin/*/tlmgr path add

# 5. Global Configuration
RUN echo '$pdf_mode = 1;' > /usr/local/texlive/latexmkrc \
    && echo '$pdflatex = "pdflatex %O -interaction=nonstopmode -synctex=1 %S";' >> /usr/local/texlive/latexmkrc

# 6. Verify Installation
CMD ["bash", "-lc", "pandoc -v && latexmk -v && pdflatex --version"]