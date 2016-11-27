# Fake News Links

_Cataloging fake news content for the public good_
 
## What is this?

This is the source code for a proof-of-concept. The idea is to set up a service where people can post URLs of fake news articles. If we create this dataset together, perhaps we can use it as a resource and learn from it. 
 
 
## Examples

- http://www.21cpw.com/shock-poll-trump-blue-collar-support-highest-since-fdr-in-1930s
- http://abcnews.com.co/amish-america-commit-vote-donald-trump-mathematically-guaranteeing-presidential-victory/
- https://70news.wordpress.com/2016/11/12/final-election-2016-numbers-trump-won-both-popular-62-9-m-62-7-m-and-electoral-college-vote-306-232-hey-change-org-scrap-your-loony-petition-now/comment-page-10/
- http://prntly.com/blog/2015/10/25/trump-successfully-pressures-ford-to-move-mexican-plant-to-ohio/
- http://prntly.com/2016/03/25/breaking-jeff-roe-cruz-adviser-may-have-greenlit-melania-ad-to-pac-admits-driving-man-to-suicide/


## Local Development

1. Create virtualenv using `virtualenv --python=python3 fake_news_links`
1. Create secret key using `export FAKENEWS_SECRET_KEY='{random_string}'`
1. Create postgres user: `createuser fakenews -P` - enter `fakenews` as password
1. Create postgres database: `createdb fakenews -O fakenews`
1. Create database url using `export FAKENEWS_DATABASE_URL='postgres://fakenews:fakenews@localhost:5432/fakenews'`


## Docker

Fake News Links is deployed using Docker containers.

Some notes on the Dockerfile:

- We're using Alpine Linux as the base since it's smaller than Ubuntu etc
- However we need build stuff to compile and install things like gevent
- uwsgi-python3 is only available on the alpine "edge" package library so we're installing all the alpine packages from there (http://dl-cdn.alpinelinux.org/alpine/edge/main/x86_64/) -- see https://pkgs.alpinelinux.org/package/edge/main/x86/uwsgi-python3
- I referenced https://github.com/jfloff/alpine-python/blob/master/3.4/Dockerfile a lot
- This was important to understand how to run uwsgi with the python plugin: http://stackoverflow.com/questions/31330905/uwsgi-options-wsgi-file-and-module-not-recognized

To build the docker image locally:

```
# first make sure we have static assets (js, images, etc.) in the right place
python manage.py collectstatic --no-input

# now build
docker build -t fake-news-links .
```

To run a container based on this image locally for testing purposes:
```
docker run -i -t --expose 8080 -p 8080:8080 -e PORT=8080 \
  -e APP_ENV=LOCAL \
  -e FAKENEWS_SECRET_KEY="somethingsecret" \
  -e FAKENEWS_DATABASE_URL="postgres://fakenews:fakenews@$(ifconfig en0 | grep inet | grep -v inet6 | cut -d ' ' -f2):5432/fakenews" \
  fake-news-links
```
