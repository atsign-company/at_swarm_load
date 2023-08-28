FROM python:3.11.5-slim

WORKDIR /usr/src/app

COPY ["docker_send_data.py", "requirements.txt", "./"]

RUN pip3 install -r requirements.txt

CMD [ "python3", "./docker_send_data.py" ]
