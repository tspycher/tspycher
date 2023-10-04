FROM python:3.11.2-bullseye

#### ENVIRONMENT
# copy the basics of the application
WORKDIR /app
ENV PIP_ROOT_USER_ACTION=ignore
ENV BUN_INSTALL="/usr/local"
# fixing issue with clourun first gen containers: https://cloud.google.com/run/docs/issues#home
ENV HOME=/root
ENV BUN_CONFIG_NO_VERIFY=1
ENV API_URL="/api"

#### COPY
COPY ./tspycher /app/tspycher
COPY ./assets /app/assets
COPY ./rxconfig.py /app/rxconfig.py
COPY ./start_rx.sh /app/start_rx.sh
COPY ./requirements.txt /app/requirements.txt

#### BASE REQUIREMENTS
# install essentials
RUN apt-get update && apt-get install -y npm nginx supervisor
RUN npm config set fund false --location=global
RUN npm install -g n
RUN n latest
RUN npm install -g bun
RUN npm install -g npm@latest
RUN npm install -g next
RUN npm install -g yarn

# prepare for nginx
RUN mkdir -p /var/log/applications
RUN mkdir -p /run/nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm -rf /etc/nginx/sites-enabled

# copy configfiles to the image
ADD etc/supervisor.ini /etc/supervisor.d/supervisor.ini
ADD etc/default.conf /etc/nginx/conf.d/default.conf

#### APPLICATION PREPARATION
# install all python packages
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt

# initalize pynecone
RUN ./start_rx.sh

# starting Service and exposing ports
CMD supervisord -n -c /etc/supervisor.d/supervisor.ini
EXPOSE 8080
EXPOSE 3000
EXPOSE 8000

