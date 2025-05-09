#!/usr/bin/env bash

# This installs the requirements on start of the devcontainer
# Just for convenience, we can remove this if you want to manually install it
# everytime you rebuild the devcontainer

mise trust -a
mise install
eval "$(mise activate bash)"

# install netshoot kubectl plugin
krew index add netshoot https://github.com/nilic/kubectl-netshoot.git
krew install netshoot/netshoot