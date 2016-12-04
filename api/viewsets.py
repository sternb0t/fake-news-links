import logging

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from api.models import FakeNewsLink, FakeNewsLinkAttribute
from api.serializers import FakeNewsLinkSerializer, FakeNewsLinkAttributeSerializer


logger = logging.getLogger(__name__)


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
    serializer_class = FakeNewsLinkSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (AnonCreateReadElseDjangoPermissions,)

    def get_queryset(self):
        query = FakeNewsLink.objects.all().prefetch_related("attributes").order_by("-created_date")
        if "attributes" in self.request.query_params:
            try:
                attribute_ids = self.request.query_params["attributes"].split(",")
                query = query.filter(attributes__pk__in=attribute_ids)
            except Exception as ex:
                logger.exception(ex)
        return query


class FakeNewsLinkAttributeViewSet(viewsets.ModelViewSet):
    queryset = FakeNewsLinkAttribute.objects.all().order_by("pk")
    serializer_class = FakeNewsLinkAttributeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
