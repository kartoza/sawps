#!/usr/bin/env bash

# This is only intended for local
# testing. See github workflows for 
# how this build is automated.

# this will create mkdocs.yml
./create-mkdocs-pdf-config.sh
# and this will build the PDF document
mkdocs build --config-file mkdocs-pdf-overview.yml > /tmp/overview-document.html
mkdocs build --config-file mkdocs-pdf-users.yml > /tmp/users-document.html
mkdocs build --config-file mkdocs-pdf-administrators.yml > /tmp/administrators-document.html
mkdocs build --config-file mkdocs-pdf-developers.yml > /tmp/developers-document.html
mkdocs build --config-file mkdocs-pdf-devops.yml > /tmp/devops-document.html
