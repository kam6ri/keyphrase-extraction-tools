ARG PYTHON_VERSION=3.9.6

FROM python:${PYTHON_VERSION}-slim-buster AS common

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MECABDIC=/var/lib/mecab/dic

WORKDIR /tmp

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Install dependencies for MeCab
    g++ \
    git \
    make \
    curl \
    xz-utils \
    file \
    patch \
    sudo \
    libmecab-dev \
    # Install MeCab
    mecab \
    # Install MeCab dictionaries
    mecab-ipadic \
    mecab-ipadic-utf8 \
    mecab-naist-jdic \
    && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /tmp/

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install poetry==1.2.0a2 && \
    poetry config virtualenvs.create false && \
    poetry install --default

###########################
# app 
###########################
FROM common AS app

ENV HOME=/app \
    PATH=$HOME/bin:$PATH

WORKDIR /tmp

RUN poetry config virtualenvs.create false && \
    poetry install --only app

# Add scripts to install additional MaCeb dictionary
COPY common/bin $HOME/bin

RUN chmod 755 $HOME/bin/*

WORKDIR $HOME/run

###########################
# jupyter
###########################
FROM common AS jupyter

ENV HOME=/jupyter \
    PATH=$HOME/bin:$PATH

WORKDIR /tmp

RUN poetry config virtualenvs.create false && \
    poetry install --only jupyter

# Add scripts to install additional MaCeb dictionary
COPY common/bin $HOME/bin

RUN chmod 755 $HOME/bin/*

WORKDIR $HOME/notebooks