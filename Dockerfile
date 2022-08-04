FROM python:3.11.0b5-slim

WORKDIR /usr/src/app

RUN pip3 install --no-cache-dir google-cloud-monitoring

COPY docker_send_data.py .

CMD [ "python3", "./docker_send_data.py" ]
