FROM python:2.7.12-alpine

# grab configs
COPY requirements.txt nginx.conf supervisor.conf /app/

# install needed packages including build dependencies
# make /usr/bin links we need for various software like supervisor
# copy config files to the right places
# install python requirements
# finally remove build dependencies
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
  && apk add --update --no-cache --virtual .build-dependencies musl=1.1.15-r5 build-base linux-headers python3-dev postgresql-dev \
  && apk add --update --no-cache python3 nginx supervisor postgresql \
  && python3 -m ensurepip \
  && rm -r /usr/lib/python*/ensurepip \
  && rm /etc/nginx/nginx.conf && cp /app/nginx.conf /etc/nginx/nginx.conf \
  && mkdir -p /etc/supervisor && cp /app/supervisor.conf /etc/supervisor/supervisord.conf \
  && pip3 install --upgrade --no-cache-dir pip \
  && pip3 install --no-cache-dir -r /app/requirements.txt \
  && apk del .build-dependencies

ENV PYTHONUNBUFFERED=1

# we assume we are running behind a load balancer so expose port 8080
EXPOSE 8080
CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]

# for debugging...
#CMD "/bin/sh"

# copy the rest of the code
COPY . /app
