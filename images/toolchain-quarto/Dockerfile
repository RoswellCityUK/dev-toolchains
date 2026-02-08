# images/toolchain-quarto/Dockerfile
ARG BASE_IMAGE=ghcr.io/roswellcityuk/dev-toolchains/base-tex:latest
FROM ${BASE_IMAGE}

# ---------------------------------------------------------------------------
# 1. CORE ESSENTIALS: Python, Jupyter, Java, Graphviz
# ---------------------------------------------------------------------------
# - python3-pip / venv: Required for Jupyter
# - default-jre-headless: Required for LTeX (grammar checking)
# - graphviz: Required for Dot/Graphviz diagrams
# - build-essential: Required to compile kernels (like Rust)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    librsvg2-bin \
    default-jre-headless \
    ghostscript \
    hunspell \
    hunspell-en-us \
    graphviz \
    python3-pip \
    python3-venv \
    build-essential \
    curl \
    gnupg \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# SETUP GLOBAL VIRTUAL ENVIRONMENT
# 1. Create the venv in /opt/venv
# 2. Add it to the PATH so 'python' and 'pip' commands automatically use it
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV \
    && chmod -R a+w $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Jupyter and libs
RUN pip install --no-cache-dir \
    jupyterlab \
    notebook \
    pandas \
    matplotlib \
    numpy \
    ipython-sql \
    sqlalchemy

# ---------------------------------------------------------------------------
# 2. RUST (Kernel: evcxr)
# ---------------------------------------------------------------------------
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && chmod -R a+w ${RUSTUP_HOME} ${CARGO_HOME} \
    && cargo install evcxr_jupyter \
    && evcxr_jupyter --install

# ---------------------------------------------------------------------------
# 3. GO (Kernel: gonb)
# ---------------------------------------------------------------------------
# Debian 12's native Go is too old for some kernels, so we fetch standard Go
ENV GOPATH=/go
ENV PATH=$GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH" \
    && GO_LATEST=$(curl -s https://go.dev/dl/?mode=json | grep -o 'go[0-9\.]*' | head -n 1) \
    && wget -q "https://go.dev/dl/${GO_LATEST}.linux-amd64.tar.gz" \
    && tar -C /usr/local -xzf "${GO_LATEST}.linux-amd64.tar.gz" \
    && rm "${GO_LATEST}.linux-amd64.tar.gz" \
    && GOBIN=/usr/local/bin go install github.com/janpfeifer/gonb@latest \
    && /usr/local/bin/gonb --install

# ---------------------------------------------------------------------------
# 4. .NET C# / F# (Kernel: .NET Interactive)
# ---------------------------------------------------------------------------
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1
ENV DOTNET_INSTALL_DIR=/usr/share/dotnet
ENV PATH=$PATH:$DOTNET_INSTALL_DIR

# Install .NET SDK
RUN curl -sSL https://dot.net/v1/dotnet-install.sh | bash /dev/stdin --channel LTS --install-dir /usr/share/dotnet \
    && ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet \
    && dotnet tool install --tool-path /usr/local/bin Microsoft.dotnet-interactive \
    && /usr/local/bin/dotnet-interactive jupyter install

# ---------------------------------------------------------------------------
# 5. QUARTO INSTALLATION
# ---------------------------------------------------------------------------
ARG QUARTO_VER="1.8.27"
RUN curl -LO "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VER}/quarto-${QUARTO_VER}-linux-amd64.deb" \
    && dpkg -i "quarto-${QUARTO_VER}-linux-amd64.deb" \
    && rm "quarto-${QUARTO_VER}-linux-amd64.deb" \
    && quarto check install

LABEL org.opencontainers.image.source=https://github.com/roswellcityuk/dev-toolchains