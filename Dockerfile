FROM python:3.10-slim
ENV DOWNLOAD_URL="https://download.acestream.media/linux/acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz"
ENV SOURCE_URL="https://api.github.com/repos/wafy80/acestream_playlist/tarball"
WORKDIR /opt/acestream
RUN apt update ; apt install -yq wget && wget -qO- $DOWNLOAD_URL | tar xz ; \
    mkdir playlist && wget -qO- $SOURCE_URL | tar xz -C playlist --strip-components=1 ; \
    pip install -q --no-cache-dir -U -r requirements.txt -r playlist/requirements.txt
EXPOSE 6878 6880
CMD ./start-engine --client-console --bind-all & \
    gunicorn -w 3 -b 0.0.0.0:6880 --chdir playlist --access-logfile search.log search:app
