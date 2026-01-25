FROM mcr.microsoft.com/devcontainers/base:bookworm

ARG DEBIAN_FRONTEND=noninteractive

# 1. Install Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    fontconfig \
    git \
    locales \
    perl \
    python3-pygments \
    wget \
    xz-utils \
    make \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    # GENERATE LOCALES (Moved from latex image to base)
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen

# 2. Install TeX Live 2025 (Optimized)
COPY texlive.profile /tmp/texlive.profile
RUN mkdir /tmp/install-tl-unx \
    && wget -qO- https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz \
    | tar -xz -C /tmp/install-tl-unx --strip-components=1 \
    && /tmp/install-tl-unx/install-tl --profile=/tmp/texlive.profile \
    # POST-INSTALL OPTIMIZATION
    && /usr/local/texlive/2025/bin/*/tlmgr option docfiles 0 \
    && /usr/local/texlive/2025/bin/*/tlmgr option srcfiles 0 \
    && /usr/local/texlive/2025/bin/*/luaotfload-tool --update \
    && rm -rf /tmp/install-tl-unx /tmp/texlive.profile

# 3. Global Configuration
ENV PATH="/usr/local/texlive/2025/bin/x86_64-linux:/usr/local/texlive/2025/bin/aarch64-linux:${PATH}"
RUN echo "export PATH=${PATH}" >> /etc/profile

# 4. Verification
RUN tlmgr --version && pdflatex --version

LABEL org.opencontainers.image.source=https://github.com/roswellcityuk/dev-toolchains
LABEL org.opencontainers.image.description="Base TeX Live 2025 Platform (Optimized + Common Tools)"