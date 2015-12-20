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
    name = models.CharField(max_length=50)
    # item statuses
    ITEM_NOT_LOST = 'NL'
    ITEM_LOST = 'L'
    ITEM_FOUND = 'F'
    ITEM_STATUS = (
        (ITEM_NOT_LOST, 'Not Lost'),
        (ITEM_LOST, 'Lost'),
        (ITEM_FOUND, 'Found'),
    )
    status = models.CharField(max_length=2, choices=ITEM_STATUS)
    is_public = models.BooleanField(default=True)
