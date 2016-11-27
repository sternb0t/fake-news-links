from rest_framework import views
from rest_framework.response import Response

from api.models import FakeNewsLink


class FakeNewsStatsView(views.APIView):

    def get(self, request, format=None):
        return Response({
            "count": FakeNewsLink.objects.count()
        })
