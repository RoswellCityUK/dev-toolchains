ARG BASE_IMAGE=ghcr.io/roswellcityuk/dev-toolchains/base-tex:latest
FROM ${BASE_IMAGE}

# Install Quarto Dependencies
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    librsvg2-bin \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Quarto
ARG QUARTO_VER="1.8.27"
RUN curl -LO "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VER}/quarto-${QUARTO_VER}-linux-amd64.deb" \
    && dpkg -i "quarto-${QUARTO_VER}-linux-amd64.deb" \
    && rm "quarto-${QUARTO_VER}-linux-amd64.deb"

# Verification
RUN quarto check install

LABEL org.opencontainers.image.source=https://github.com/roswellcityuk/dev-toolchains
LABEL org.opencontainers.image.description="Quarto Publishing Toolchain"