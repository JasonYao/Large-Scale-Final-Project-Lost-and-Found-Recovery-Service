from __future__ import unicode_literals

from django.db import models

# Create your models here.
class FinderUser(models.Model):
	user_id = models.BigIntegerField(primary_key=True)
	username = models.CharField(max_length=30, unique=True)
	email = models.CharField('email address', max_length=30, blank=True)

class Item(models.Model):
	user_id = models.BigIntegerField(db_index=True)
	item_id = models.BigIntegerField(db_index=True)
  	name = models.CharField(max_length=256)
