FROM python:3.10-slim
ENV DOWNLOAD_URL="https://download.acestream.media/linux/acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz"
WORKDIR /opt/acestream
RUN apt update && apt install -y wget && wget -q -c $DOWNLOAD_URL -O - | tar -xz ; \
    pip install --no-cache-dir --upgrade --requirement requirements.txt
EXPOSE 6878
ENTRYPOINT ["./start-engine"] 
CMD ["--client-console","--live-cache-type memory","--bind-all"]