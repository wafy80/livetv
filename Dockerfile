FROM python:slim
ENV TZ="Europe/Rome"
WORKDIR /opt/livetv
COPY . .
RUN apt update ; apt install -yq procps tor locales ; \
    pip install -q --no-cache-dir -U -r requirements.txt ; \
    sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
EXPOSE 6880
CMD ["gunicorn", "-w", "3", "-b", "[::]:6880", "--access-logfile", "search.log", "search:app"]
