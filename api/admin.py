from django.contrib import admin

from api.models import FakeNewsLink


class FakeNewsLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'created_date', 'updated_date')
    ordering = ('-created_date',)

admin.site.register(FakeNewsLink, FakeNewsLinkAdmin)
