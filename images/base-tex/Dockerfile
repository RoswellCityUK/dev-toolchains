# images/base-tex/Dockerfile
FROM mcr.microsoft.com/devcontainers/base:bookworm

# Silence apt warnings
ARG DEBIAN_FRONTEND=noninteractive

# 1. Install Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    fontconfig \
    git \
    locales \
    make \
    perl \
    python3-pygments \
    wget \
    xz-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen

# 2. Set PATH (Simpler now: only x86_64)
ENV PATH="/usr/local/texlive/2025/bin/x86_64-linux:${PATH}"
RUN echo "export PATH=${PATH}" >> /etc/profile

# 3. Install TeX Live 2025
COPY texlive.profile /tmp/texlive.profile
RUN mkdir /tmp/install-tl-unx \
    && wget -qO- https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz \
    | tar -xz -C /tmp/install-tl-unx --strip-components=1 \
    && /tmp/install-tl-unx/install-tl --profile=/tmp/texlive.profile \
    # Cleanup & Setup
    && tlmgr option docfiles 0 \
    && tlmgr option srcfiles 0 \
    && luaotfload-tool --update \
    && rm -rf /tmp/install-tl-unx /tmp/texlive.profile

# 4. Verification
RUN tlmgr --version && pdflatex --version

LABEL org.opencontainers.image.source=https://github.com/roswellcityuk/dev-toolchains
LABEL org.opencontainers.image.description="Base TeX Live 2025 Platform (AMD64 Only)"