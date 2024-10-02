FROM python:3.10-slim
ENV TZ="Europe/Rome"
ENV DOWNLOAD_URL="https://download.acestream.media/linux/acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz"
WORKDIR /opt/acestream
COPY . playlist
RUN apt update ; apt install -yq procps tor locales wget && wget -qO- $DOWNLOAD_URL | tar xz ; \
    pip install -q --no-cache-dir -U -r requirements.txt -r playlist/requirements.txt ; \
    sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
EXPOSE 6878 6880
WORKDIR /opt/acestream/playlist
CMD /opt/acestream/start-engine --client-console --bind-all & \
    python3 livetv.py & python3 cron.py & \
    gunicorn -w 3 -b 0.0.0.0:6880 --access-logfile search.log search:app
