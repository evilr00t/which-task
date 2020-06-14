import pytest
import requests
import os
from requests.exceptions import ConnectionError


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "docker-compose.yml")

def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False

@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("which-proxy", 8000)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=10.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url

@pytest.fixture(scope="session")
def proxy_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("which-proxy", 8080)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=10.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url

def test_monitoring_status_code(http_service):
    status = 200
    response = requests.get(http_service)
    assert response.status_code == status

def test_monitoring_encoding(http_service):
    content_type = 'application/json'
    response = requests.get(http_service)
    assert response.headers.get('content-type') == content_type

def test_monitoring_content(http_service):
    response = requests.get(http_service).json()
    # response = response.json()
    assert response['last_generated'] is not None and \
    response['hostname'] is not None and \
    response['memory_usage_in_mb'] is not None and \
    response['processes_num'] is not None and \
    response['processes'] is not None and \
    response['processes'][0]['cpu_percent'] is not None and \
    response['processes'][0]['name'] is not None and \
    response['processes'][0]['pid'] is not None and \
    response['disk_usage_in_mb'] is not None

def test_proxy_user_agent(proxy_service):
    url = "http://httpbin.org/get"
    proxies = {
        "https": proxy_service,
        "http": proxy_service
    }
    r = requests.get(url, proxies=proxies, verify=False).json()
    assert r['headers']['User-Agent'] == 'FooBar'

def test_proxy_removed_header(proxy_service):
    url = "http://httpbin.org/get"
    proxies = {
        "https": proxy_service,
        "http": proxy_service
    }
    r = requests.get(url, proxies=proxies, verify=False).json()
    assert 'Accept' not in r['headers']