#!/usr/bin/env bash
set -e

# Install dependencies
pip install -r requirements.txt

# Ensure avatars directory exists (for donor avatars)
mkdir -p static/images/avatars
