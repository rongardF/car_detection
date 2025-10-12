# syntax = docker/dockerfile:1.0-experimental
FROM python:3.12 AS base

RUN mkdir -p /opt/app

ENV PYTHONPYCACHEPREFIX=/tmp/pycache

# install python libraries using cache to speed-up subsequent build process
COPY requirements.txt /tmp/

RUN --mount=type=cache,target=/root/.cache/pip  \
    pip install -r /tmp/requirements.txt

RUN apt-get update
RUN apt-get install libgl1 -y

FROM base AS devcontainer

# install packages for dev
COPY .devcontainer/requirements.dev.txt /tmp/

RUN --mount=type=cache,target=/root/.cache/pip  \
    pip install -r /tmp/requirements.dev.txt

# copy everything
COPY ./ /opt/app

ENV PYTHONPATH="$PYTHONPATH:/opt/app/src"

WORKDIR /opt/app

FROM base AS production

# remove requirements file
RUN rm /tmp/requirements.txt

# copy everything from src
COPY ./src /opt/app/src

# add non-root user and disable the login for that user
RUN adduser --disabled-password --disabled-login --gecos "" app

# change app directory ownership to allow non-root user access
RUN chown app:app /opt/app

WORKDIR /opt/app/src

# change from root user to non-root user (commands after this are run as 'app' user)
USER app
