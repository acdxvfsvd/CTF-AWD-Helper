# CTF-AWD Helper

A Simple Platform for Attack-with-Defense style CTF competitions.

## Features

- Asynchronous flag submitter

## Requirements

- Python 3
- Flask
- Redis
- Celery

## Usage

```shell
# set up a local redis server
redis-server
# celery daemon
celery -A app.celery worker -E
# flask app
flask run
```

## TODO

- Pcap Analyzer & Script Generator
- Flag validation in proxy
