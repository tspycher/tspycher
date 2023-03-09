FROM python:3.11.2-bullseye

WORKDIR /app
COPY ./tspycher /app/tspycher
COPY ./assets /app/assets
COPY ./pcconfig.py /app/pcconfig.py
COPY ./requirements.txt /app/requirements.txt


RUN apt-get update && apt-get install -y nodejs nginx supervisor

RUN mkdir -p /var/log/applications
RUN mkdir -p /run/nginx

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm -rf /etc/nginx/sites-enabled

ADD etc/supervisor.ini /etc/supervisor.d/supervisor.ini
ADD etc/default.conf /etc/nginx/conf.d/default.conf

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pc init

#fixing issue with cloud run
RUN mkdir -p /home/.bun/bin
RUN ln -s /root/.bun/bin/bun /home/.bun/bin/bun

# Starting Service
CMD supervisord -n -c /etc/supervisor.d/supervisor.ini

EXPOSE 8080
EXPOSE 3000
EXPOSE 8000

