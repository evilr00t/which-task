import os
from jinja2 import Environment

SET_HEADERS = os.environ.get("SET_HTTP_HEADERS", [])
UNSET_HEADERS = os.environ.get("UNSET_HTTP_HEADERS", [])


def generate_config():
    set_headers = []
    unset_headers = []
    if SET_HEADERS:
        set_headers = [x.lstrip() for x in SET_HEADERS.split(',')]
    if UNSET_HEADERS:
        unset_headers = [x.lstrip() for x in UNSET_HEADERS.split(',')]
    env = Environment()
    tmpl = env.from_string(
        """
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_connect_module modules/mod_proxy_connect.so
LoadModule proxy_http_module modules/mod_proxy_http.so
LoadModule ssl_module modules/mod_ssl.so

Listen 8080

<VirtualHost *:8080>
ProxyRequests On

<Proxy *>
    # ACL
    # Order Deny,Allow
    # Deny from all
    # Allow from 192.168.0.20
</Proxy>

# Monitoring
<Location "/status">
  ProxyPass "http://localhost:8000"
</Location>

{% if unset_headers is not none %}
{% for header in unset_headers -%}
RequestHeader unset {{ header }}
{% endfor %}
{% endif %}
{% if set_headers is not none %}
{% for header in set_headers -%}
RequestHeader set {{ header }}
{% endfor %}
{% endif %}
</VirtualHost>
    """
    )

    print(tmpl.render(set_headers=set_headers, unset_headers=unset_headers))


generate_config()
