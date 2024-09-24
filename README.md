# stock_digest

[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](#)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Creates a configurable summary of stock movements to your inbox:

![Stock Digest](https://i.imgur.com/QaE9Ejq.png)

## Setup
- Install:
    - `git clone https://github.com/lucashadfield/stock_digest.git`
    - `cd stock_digest`
    - `pip install --upgrade .`
- Config:
    - `cp stocks.yaml ~/.config/stock_digest/.`
        - edit `~/.config/stock_digest/stocks.yaml` for desired config
    - `cp email.yaml ~/.config/stock_digest/.`
        - edit `~/.config/stock_digest/email.yaml` for gmail config
        - Gmail requires the sender to be configured as a "[Less secure app](https://support.google.com/accounts/answer/6010255?hl=en)"
        - I recommend setting up a separate email address for this purpose
- Run:
    - `stock_digest` - run for today
    - `stock_digest 2020-10-01` - run a specific day

## Docker
- `chmod +x build.sh`
- `./build.sh`