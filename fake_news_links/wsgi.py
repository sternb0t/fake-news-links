"""
WSGI config for fake_news_links project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
from gevent import monkey
monkey.patch_all()
import psycogreen.gevent
psycogreen.gevent.patch_psycopg()

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fake_news_links.settings")

application = get_wsgi_application()
