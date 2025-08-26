FROM python:3.14.0rc2-alpine3.22

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config.json .
COPY hetznerDNS.py .
COPY logging.yaml .

CMD [ "python", "./hetznerDNS.py" ]