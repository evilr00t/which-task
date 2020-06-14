FROM httpd:2.4.43

LABEL MAINTANER="k@e-dot.uk"

ENV SET_HTTP_HEADER ""
ENV UNSET_HTTP_HEADER ""
ENV STATUS_REFRESH_PERIOD 5

# Add python3 and psutil package needed by our little monitoring script
RUN apt update && \
    apt -y install --no-install-recommends python3-psutil python3-jinja2 procps && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Proxy config
# COPY proxy.conf /usr/local/apache2/conf/proxy.conf
COPY config-generator.py /opt/config-generator.py

# Monitoring script
COPY monitoring.py /opt/monitoring.py
COPY start.sh /start.sh

# Enable proxy config in httpd.conf
RUN echo 'Include conf/proxy.conf' >> /usr/local/apache2/conf/httpd.conf

# Mostly as FYI as this is not really usable
EXPOSE 8080 8000

CMD ["/start.sh"]
