from django.conf.urls import url

from web import views as web_views

urlpatterns = [
    url(r'^', web_views.index, name="index"),
]
