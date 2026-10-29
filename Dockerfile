FROM python:3.15.0-slim@sha256:f5b92f2a669a4c347044f29367f31983280b648250ca94dea66f98c53bc87e58

WORKDIR /usr/src/app

COPY ["docker_send_data.py", "requirements.txt", "./"]

RUN pip3 install -r requirements.txt

CMD [ "python3", "./docker_send_data.py" ]
