FROM python:3.11.2-bullseye

# copy the basics of the application
WORKDIR /app

# fixing issue with clourun first gen containers: https://cloud.google.com/run/docs/issues#home
CMD HOME=/root

COPY ./tspycher /app/tspycher
COPY ./assets /app/assets
COPY ./pcconfig.py /app/pcconfig.py
COPY ./requirements.txt /app/requirements.txt

# install essentials
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get update && apt-get install -y \
    nodejs \
    unzip \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/* \
RUN npm install next react react-dom
RUN echo "alias next='npx next'" >> ~/.bashrc

# prepare for nginx
RUN mkdir -p /var/log/applications
RUN mkdir -p /run/nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm -rf /etc/nginx/sites-enabled

# copy configfiles to the image
ADD etc/supervisor.ini /etc/supervisor.d/supervisor.ini
ADD etc/default.conf /etc/nginx/conf.d/default.conf

# install all python packages
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt

# initalize pynecone
ENV BUN_INSTALL="/app/.bun"
RUN pc init

# fixing issue with cloud run not finding BUN
#RUN mkdir -p /home/.bun/bin
RUN mkdir -p /root/.bun/bin
#RUN ln -s /app/.bun/bin/bun /home/.bun/bin/bun
RUN ln -s /app/.bun/bin/bun /root/.bun/bin/bun

# starting Service and exposing ports
CMD supervisord -n -c /etc/supervisor.d/supervisor.ini
EXPOSE 8080
EXPOSE 3000
EXPOSE 8000

