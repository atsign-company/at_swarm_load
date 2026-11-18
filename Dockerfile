FROM python:3.15.2-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

WORKDIR /usr/src/app

COPY ["docker_send_data.py", "requirements.txt", "./"]

RUN pip3 install -r requirements.txt

CMD [ "python3", "./docker_send_data.py" ]
