from rest_framework import routers

from api import viewsets as api_viewsets

fake_news_router = routers.DefaultRouter()
fake_news_router.register(r'links', api_viewsets.FakeNewsLinkViewSet, base_name="fakenews-links")
fake_news_router.register(r'attributes', api_viewsets.FakeNewsLinkAttributeViewSet, base_name="fakenews-attributes")
