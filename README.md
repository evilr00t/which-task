# README

## Usage

```sh
docker build . -t apache-proxy
docker run --rm -it -p 8000:8000 -p 8080:8080 -e SET_HTTP_HEADERS="User-Agent: TechTest, X-Foo: Bar" -e UNSET_HTTP_HEADERS="Agent, Encoding" --name proxy apache-proxy
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