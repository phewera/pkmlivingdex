#!/usr/bin/env bash
echo "Setting up Python virtualenv ..."
virtualenv -p python3.12 ./.venv/

echo "Installing requirements ..."
./.venv/bin/pip install -r ./requirements.txt
