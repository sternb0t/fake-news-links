from django.db import models


class DateTracking(models.Model):
    """
    An abstract model that adds tracking fields for creation and modification dates
    """
    created_date = models.DateTimeField(blank=False, null=False,
                                        auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(blank=False, null=False,
                                        auto_now=True, db_index=True)

    class Meta:
        abstract = True
