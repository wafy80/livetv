FROM wafy80/acestream
WORKDIR /opt/acelist
COPY *.py *.txt *.sh .
RUN pip install --no-cache-dir --upgrade --requirement requirements.txt
EXPOSE 6880
ENTRYPOINT ./start.sh