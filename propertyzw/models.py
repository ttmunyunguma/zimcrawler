from django.db import models


class Property(models.Model):
    usd_price = models.CharField(max_length=255)
    zwl_price = models.CharField(max_length=255)
    prop_title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    detail = models.TextField()
    link = models.CharField(max_length=255)

    class Meta:
        db_table = 'property'
