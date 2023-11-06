![python](https://img.shields.io/badge/Python-3.12-blue)
[![main](https://github.com/phewera/pkmlivingdex/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/phewera/pkmlivingdex/actions/workflows/main.yml)

# Pokemon Living Dex

## Install dependencies

### Python
```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3-pip
sudo pip3 install virtualenv 
```

## Run with docker

TODO

## Run local

### Install backend

#### Run `bootstrap.sh`

```shell
cd backend
./bootstrap.sh
```

### Install frontend

TODO

### Start services

TODO

## Importer

TODO

## Development

### Run unittests

```shell
cd backend
./bootstrap.sh
source .venv/bin/activate
python testing.py
```