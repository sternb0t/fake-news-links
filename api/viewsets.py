from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from api import models as api_models
from api import serializers as api_serializers


class AnonCreateReadElseDjangoPermissions(DjangoModelPermissionsOrAnonReadOnly):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class FakeNewsLinkViewSet(viewsets.ModelViewSet):
    queryset = api_models.FakeNewsLink.objects.all().order_by("-created_date")
    serializer_class = api_serializers.FakeNewsLinkSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (AnonCreateReadElseDjangoPermissions,)
