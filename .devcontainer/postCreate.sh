#!/usr/bin/env bash

echo 'eval "$(mise activate zsh)"' >> ~/.zshrc
echo 'eval "$(mise activate bash)"' >> ~/.bashrc
echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >> ~/.zshrc
