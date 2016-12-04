from django.db import models

from common.models import DateTracking


class FakeNewsLinkAttribute(DateTracking):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}: {}".format(self.pk, self.name)


class FakeNewsLink(DateTracking):
    url = models.URLField(max_length=1000)
    latitude = models.DecimalField(blank=True, null=True, decimal_places=6, max_digits=9)
    longitude = models.DecimalField(blank=True, null=True, decimal_places=6, max_digits=9)
    geo_accuracy = models.DecimalField(blank=True, null=True, decimal_places=0, max_digits=9)
    attributes = models.ManyToManyField(FakeNewsLinkAttribute, blank=True)

    def __str__(self):
        return "{}: {}".format(self.pk, self.url)
