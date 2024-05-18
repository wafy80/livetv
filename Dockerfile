FROM wafy80/acestream
ENV RAW_URL="https://raw.githubusercontent.com/Wafy80/acestream_playlist/master"
WORKDIR /opt/acelist
RUN wget -q $RAW_URL/search.py $RAW_URL/acestream_search.py $RAW_URL/requirements.txt ; \
    pip install --no-cache-dir --upgrade --requirement requirements.txt
EXPOSE 6880
ENTRYPOINT ["python3"]
CMD ["search.py"]