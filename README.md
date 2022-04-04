# KET: Keyphrase Extraction Tools

### Create and start docker containers

```shell
# It takes very long time
> docker-compose up -d --build

# (Recommended) You can also use a docker image that contains all necessary dependencies
> docker-compose -f docker-compose.simple.yml up -d --build
```

This command will start two containers.

- `app` container provides services for web applications.
- `jupyter` container provides an interactive development environment using jupyterlab.

Check if these services are up and running.
- `app`: [`localhost:8501`](localhost:8501)
- `jupyter`: [`localhost:8888`](localhost:8888)

### Install additional dictionary for MeCab

```shell
> docker-compose exec [app|jupyter] install-mecabdic
```

Installed dictionaries (`$MECABDIC=/var/lib/mecab/dic`) are shared by `app` and `jupyter`.

### Shutdown and remove containers

```shell
> docker-compose down
```