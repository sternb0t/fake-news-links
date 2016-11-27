from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField

from common.models import DateTracking


class User(DateTracking, AbstractUser):
    """
    Django model for an individual user that has some kind of access to Fake News Links.
    This could be admin or lower level access.

    For now we are mostly using the fields present in Django's AbstractUser.
    Since we are using postgres, we add a JSON data store (user.data) for arbitrary key-value properties.
    """
    data = JSONField(blank=True, null=True)
