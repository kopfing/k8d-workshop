FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# MISE based on https://mise.jdx.dev/mise-cookbook/docker.html
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV MISE_DATA_DIR="/mise"
ENV MISE_CONFIG_DIR="/mise"
ENV MISE_CACHE_DIR="/mise/cache"
ENV MISE_INSTALL_PATH="/usr/local/bin/mise"
# Shims are better for non-interactive shells, 
# we use the eval "$(mise activate zsh)" in the zshrc from devcontainer.json instead
#ENV PATH="/mise/shims:$PATH"  
ENV MISE_VERSION="v2025.5.5"

RUN curl https://mise.run | sh && \
    mkdir -p $MISE_DATA_DIR $MISE_CONFIG_DIR $MISE_CACHE_DIR && \
    chmod -R 777 $MISE_DATA_DIR

RUN apt-get update && \
    apt-get install -y iputils-ping dnsutils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# needed to surpress warning in devcontainer
ENV UV_LINK_MODE=copy

# create alias for kubectl
RUN echo "alias k='kubectl'" >> /etc/bash.bashrc && \
    echo "alias k='kubectl'" >> /etc/zsh/zshrc

