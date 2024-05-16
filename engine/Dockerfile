FROM ubuntu:22.04
ENV DOWNLOAD_URL="https://download.acestream.media/linux/acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz"
RUN apt update && apt install -y --no-install-recommends python3.10 libpython3.10 python3-pip curl && apt clean ; \
    mkdir /opt/acestream && cd /opt/acestream && curl $DOWNLOAD_URL | tar xzf - ; \
    pip install --no-cache-dir --upgrade --requirement requirements.txt
EXPOSE 6878
ENTRYPOINT ["/opt/acestream/start-engine","--client-console","--live-cache-type memory","--bind-all"]