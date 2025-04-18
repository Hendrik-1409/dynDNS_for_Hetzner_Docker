FROM python:3.13.0-alpine3.20

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config.json .
COPY hetznerDNS.py .
COPY logging.config .

CMD [ "python", "./hetznerDNS.py" ]