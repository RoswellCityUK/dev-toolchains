FROM ghcr.io/roswellcityuk/dev-toolchains/base-tex:latest

# Install Quarto Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    librsvg2-bin \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Quarto (Dynamic Architecture)
RUN QUARTO_VER="1.8.27" \
    && ARCH=$(dpkg --print-architecture) \
    && curl -LO "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VER}/quarto-${QUARTO_VER}-linux-${ARCH}.deb" \
    && dpkg -i "quarto-${QUARTO_VER}-linux-${ARCH}.deb" \
    && rm "quarto-${QUARTO_VER}-linux-${ARCH}.deb"

# Verification & Metadata
RUN quarto check install
LABEL org.opencontainers.image.source=https://github.com/roswellcityuk/dev-toolchains
LABEL org.opencontainers.image.description="Quarto Publishing Toolchain"