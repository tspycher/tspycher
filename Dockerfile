FROM python:3.11.2-bullseye

WORKDIR /app
COPY ./tspycher /app/tspycher
COPY ./assets /app/assets
COPY ./pcconfig.py /app/pcconfig.py
COPY ./requirements.txt /app/requirements.txt


RUN apt-get update && apt-get install -y nodejs

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pc init

CMD ["pc","run" , "--env", "prod"]

EXPOSE 3000
EXPOSE 8000