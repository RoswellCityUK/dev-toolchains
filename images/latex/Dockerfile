# Stage 1: Upstream TeX Live
# We pull the official image which contains the full, latest TeX Live scheme.
FROM texlive/texlive:latest AS tex

# OPTIMIZATION: Remove docs and source code.
# This reduces the copy size by approx 3GB, trying to prevent disk exhaustion in github runner.
RUN rm -rf /usr/local/texlive/*/texmf-dist/doc \
    && rm -rf /usr/local/texlive/*/texmf-dist/source

# Stage 2: Your Dev Container
FROM mcr.microsoft.com/devcontainers/base:bookworm

LABEL org.opencontainers.image.source=https://github.com/roswellcityuk/dev-toolchains
LABEL org.opencontainers.image.description="LaTeX Dev Container based on Debian Bookworm (latest TeX Live)"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# 1. Install System Dependencies
# We removed 'texlive-*', 'biber', and 'latexmk' from apt because
# they are included in the official TeX Live distribution we are copying.
# We keep tools like git, make, pygments (for minted), and perl (required by latexmk/tlmgr).
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    make \
    perl \
    python3-pygments \
    ghostscript \
    pandoc \
    hunspell \
    hunspell-en-us \
    poppler-utils \
    libyaml-tiny-perl \
    libfile-homedir-perl \
    default-jre-headless \
    # locales are often needed for proper font encoding
    locales \
  && apt-get clean && rm -rf /var/lib/apt/lists/* \
  && locale-gen en_US.UTF-8

# 2. Copy TeX Live from Stage 1
# This copies the entire TeX Live directory (usually /usr/local/texlive)
COPY --from=tex /usr/local/texlive /usr/local/texlive

# 3. Link TeX Live to your PATH
# 'tlmgr path add' automatically symlinks the binaries (pdflatex, biber, latexmk, etc.)
# from the year-specific folder to /usr/local/bin.
RUN /usr/local/texlive/*/bin/*/tlmgr path add

# 4. Global Configuration
# Set default latexmk behavior: output PDF, don't stop on error
RUN echo '$pdf_mode = 1;' > /usr/local/texlive/latexmkrc \
    && echo '$pdflatex = "pdflatex %O -interaction=nonstopmode -synctex=1 %S";' >> /usr/local/texlive/latexmkrc

# 5. Verify Installation
# We check version output to confirm we are on the latest year.
CMD ["bash", "-lc", "latexmk -v && pdflatex --version && biber --version"]