FROM python:3.10
ENV DOWNLOAD_URL="https://download.acestream.media/linux/acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz"
RUN mkdir -p /opt/acestream ; \
    cd /opt/acestream ; \
    curl $DOWNLOAD_URL | tar xzf - ; \
    pip install --no-cache-dir --upgrade --requirement requirements.txt
EXPOSE 6878
ENTRYPOINT ["/opt/acestream/start-engine","--client-console","--live-cache-type memory","--bind-all"]