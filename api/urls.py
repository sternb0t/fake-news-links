from django.conf.urls import url, include

from api import routers as api_routers
from api import views as api_views

urlpatterns = [
    url(r'^', include(api_routers.fake_news_router.urls)),
    url(r'^stats/', api_views.FakeNewsStatsView.as_view(), name='stats')
]
