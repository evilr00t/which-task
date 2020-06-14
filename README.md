# README

![CircleCI](https://circleci.com/gh/evilr00t/which-task.svg?style=svg&circle-token=78420d96ea29c9e5185dde6ea7542e385827f54a)


## Usage (Not for production)

```sh
docker build . -t apache-proxy
docker run --rm -it -p 8000:8000 -p 8080:8080 -e SET_HTTP_HEADER="User-Agent: FooBar" -e UNSET_HTTP_HEADER="Accept" -e STATUS_REFRESH_PERIOD=10 --name proxy apache-proxy
```

## Status page

Status page is available from two endpoints:
 * http://container_ip:8000
 * http://container_ip:8080/status

It will return JSON with all required information.

## Tests
Tests are done using pytest-docker

```sh
pip3 install pytest-docker pytest requests
```

should sort out requirements. Then you can run `pytest tests.py` and integration tests should start.

## Variables

Local environmental variables accepted by Docker image.

`SET_HTTP_HEADER` - a list of http headers that will be added or overwritten (if already set) by proxy
`UNSET_HTTP_HEADER` - a list of http headers that will be removed by proxy

`STATUS_REFRESH_PERIOD` - number - refresh rate for our status page (in seconds) - default is 5

