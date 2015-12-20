from __future__ import unicode_literals

from django.db import models

# Create your models here.
class FinderUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField('email address', max_length=256, blank=True)


class Item(models.Model):
    item_id = models.BigIntegerField(primary_key=True)
    owner = models.ForeignKey(FinderUser, on_delete=models.CASCADE)
    qr_code = models.CharField(max_length=256)
    name = models.CharField(max_length=50)
    ITEM_STATUS = (
        ('NL', 'Not Lost'),
        ('L', 'Lost'),
        ('F', 'Found'),
    )
    status = models.CharField(max_length=2, choices=ITEM_STATUS)
    is_public = models.BooleanField(default=True)



