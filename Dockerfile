FROM python:3.10-slim
ENV DOWNLOAD_URL="https://download.acestream.media/linux/acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz"
ENV SOURCE_URL="https://api.github.com/repos/wafy80/acestream_playlist/tarball"
WORKDIR /opt/acestream
RUN apt update ; apt install -y wget && wget -qO- $DOWNLOAD_URL | tar xz ; \
    pip install --no-cache-dir --upgrade --requirement requirements.txt 
EXPOSE 6878 6880
CMD mkdir playlist && cd playlist ; \
    wget -qO- $SOURCE_URL | tar xz --strip-components=1 ; chmod +x start.sh ; \
    pip install --no-cache-dir --upgrade --requirement requirements.txt ; \
    ./start.sh