from django.contrib import admin

from api.models import FakeNewsLink, FakeNewsLinkAttribute


class FakeNewsLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'latitude', 'longitude', 'geo_accuracy', 'created_date', 'updated_date')
    ordering = ('-created_date',)

admin.site.register(FakeNewsLink, FakeNewsLinkAdmin)


class FakeNewsLinkAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_date', 'updated_date')
    ordering = ('id',)

admin.site.register(FakeNewsLinkAttribute, FakeNewsLinkAttributeAdmin)
