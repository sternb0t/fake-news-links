from rest_framework import serializers
from rest_framework_cache.serializers import CachedSerializerMixin
from rest_framework_cache.registry import cache_registry
from rest_framework.fields import empty

from api.models import FakeNewsLink, FakeNewsLinkAttribute


class FakeNewsLinkAttributeSerializer(serializers.HyperlinkedModelSerializer, CachedSerializerMixin):

    class Meta:
        model = FakeNewsLinkAttribute
        fields = ('id', 'name', 'created_date', 'updated_date')
        read_only_fields = ('id', 'created_date',)

cache_registry.register(FakeNewsLinkAttributeSerializer)


class FakeNewsLinkAttributeSimpleSerializer(serializers.HyperlinkedModelSerializer, CachedSerializerMixin):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)

    class Meta:
        model = FakeNewsLinkAttribute
        fields = ('id', 'name',)
        read_only_fields = ('id', 'name',)

cache_registry.register(FakeNewsLinkAttributeSimpleSerializer)


class FakeNewsLinkSerializer(serializers.HyperlinkedModelSerializer):
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    geo_accuracy = serializers.FloatField(required=False)
    attributes = FakeNewsLinkAttributeSimpleSerializer(many=True, required=False)

    class Meta:
        model = FakeNewsLink
        fields = ('id', 'url', 'latitude', 'longitude', 'geo_accuracy', 'attributes', 'created_date', 'updated_date')
        read_only_fields = ('id', 'created_date',)

    def create(self, validated_data):
        if "attributes" in validated_data:
            attributes = validated_data.pop("attributes")
            link = FakeNewsLink.objects.create(**validated_data)
            for attribute in attributes:
                if "id" in attribute:
                    try:
                        fake_news_link_attribute = FakeNewsLinkAttribute.objects.get(pk=attribute["id"])
                    except Exception:
                        pass
                    else:
                        link.attributes.add(fake_news_link_attribute)
        else:
            link = FakeNewsLink.objects.create(**validated_data)
        return link
