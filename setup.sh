#!/bin/bash

# install python

START_DIR=$(pwd)

sudo apt-get update && sudo apt-get install -y build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev wget curl llvm libbz2-dev && (dpkg -l | grep -q python3-venv || sudo apt-get install -y python3-venv) && wget https://www.python.org/ftp/python/3.11.2/Python-3.11.2.tgz && tar -xf Python-3.11.2.tgz && cd Python-3.11.2 && ./configure --enable-optimizations && make -j "$(nproc)" && sudo make altinstall

cd "$START_DIR"

# create python venv and install modules

PYTHON_BIN=/usr/local/bin/python3.11

$PYTHON_BIN -m venv python

source python/bin/activate

python -m ensurepip --upgrade

pip install --no-cache-dir pygame pyinstaller pillow numpy hjson
