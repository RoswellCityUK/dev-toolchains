FROM mcr.microsoft.com/devcontainers/base:bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Core TeX + tooling used by LaTeX Workshop (latexmk) and biblatex (biber).
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    make \
    latexmk \
    texlive \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-bibtex-extra \
    biber \
    texlive-science \
    texlive-pictures \
    texlive-extra-utils \
    python3-pygments \
    ghostscript \
    poppler-utils \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Non-fatal: some images don't need or support a full fmt run, but it helps when available.
RUN fmtutil-sys --all || true

# A tiny sanity check layer (doesn't run at build time, but documents what's expected)
CMD ["bash", "-lc", "latexmk -v && pdflatex --version && biber --version"]
