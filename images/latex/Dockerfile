# syntax=docker/dockerfile:1.7

# Stage 1: Upstream TeX Live
FROM --platform=$TARGETPLATFORM texlive/texlive:latest AS tex

# Remove docs and sources (biggest space saver)
RUN rm -rf /usr/local/texlive/*/texmf-dist/doc \
           /usr/local/texlive/*/texmf-dist/source

# Optional: remove tlmgr caches/backups/logs (often non-trivial)
RUN rm -rf /usr/local/texlive/*/texmf-var/tlpkg/backups \
           /usr/local/texlive/*/texmf-var/tlpkg/tlpg \
           /usr/local/texlive/*/texmf-var/web2c/*.log \
           /usr/local/texlive/*/tlpkg/texlive.tlpdb.* || true

# Stage 2: Dev container
FROM mcr.microsoft.com/devcontainers/base:bookworm

LABEL org.opencontainers.image.source=https://github.com/roswellcityuk/dev-toolchains
LABEL org.opencontainers.image.description="LaTeX Dev Container based on Debian Bookworm (latest TeX Live)"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Faster apt with BuildKit cache mounts (no effect if BuildKit disabled)
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
      git \
      make \
      perl \
      python3-pygments \
      ghostscript \
      hunspell \
      hunspell-en-us \
      poppler-utils \
      libyaml-tiny-perl \
      libfile-homedir-perl \
      default-jre-headless \
      locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# Copy TeX Live tree
# --link helps on BuildKit-enabled builders (less I/O during build)
COPY --from=tex --link /usr/local/texlive /usr/local/texlive

# Resolve the newest TL year + arch bin dir once, then set PATH
# Also good for shells: drop a profile.d script
RUN set -eux; \
    TL_YEAR="$(ls -1 /usr/local/texlive | sort -r | head -n1)"; \
    TL_BIN="$(ls -d /usr/local/texlive/${TL_YEAR}/bin/* | head -n1)"; \
    echo "export PATH=${TL_BIN}:\$PATH" > /etc/profile.d/texlive.sh; \
    chmod +x /etc/profile.d/texlive.sh; \
    # sanity check
    "${TL_BIN}/latexmk" -v

# Global Configuration
RUN printf '%s\n' \
    '$pdf_mode = 1;' \
    '$pdflatex = "pdflatex %O -interaction=nonstopmode -synctex=1 %S";' \
    > /usr/local/texlive/latexmkrc

# Ensure PATH is correct for non-login shells too
# (the value is expanded at build time via /etc/profile.d for interactive shells,
# but ENV is what actually matters for RUN/CMD)
RUN set -eux; \
    TL_YEAR="$(ls -1 /usr/local/texlive | sort -r | head -n1)"; \
    TL_BIN="$(ls -d /usr/local/texlive/${TL_YEAR}/bin/* | head -n1)"; \
    echo "TL_BIN=${TL_BIN}" > /tmp/tlbin.env
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
# (Build-time computed PATH is tricky to inject directly into ENV in pure Dockerfile,
# but the /etc/profile.d script handles interactive use; CMD below uses bash -lc anyway.)

CMD ["bash", "-lc", "latexmk -v && pdflatex --version && biber --version"]
