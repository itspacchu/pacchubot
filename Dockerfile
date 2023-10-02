from python:3.9-slim-bookworm

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /pacbot

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3 main.py" ]