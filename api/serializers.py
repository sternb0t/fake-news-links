from rest_framework import serializers

from api.models import FakeNewsLink


class FakeNewsLinkSerializer(serializers.HyperlinkedModelSerializer):
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    geo_accuracy = serializers.FloatField(required=False)

    class Meta:
        model = FakeNewsLink
        fields = ('id', 'url', 'latitude', 'longitude', 'geo_accuracy', 'created_date', 'updated_date')
        read_only_fields = ('id', 'created_date',)
