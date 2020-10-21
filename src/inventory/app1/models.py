from django.db import models

# Create your models here.
class rack(models.Model):

    name = models.CharField(max_length=100)
    slots = models.IntegerField(default=0)
    occSlot = models.IntegerField(default=0)
    description = models.CharField(max_length=500,default='none')

class items(models.Model):

    name = models.CharField(max_length=100)
    itemID = models.CharField(max_length=50)
    seralID = models.CharField(max_length=50)
    description = models.CharField(max_length=500,default='none')
    status = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    rack = models.CharField(max_length=500,default="o")

class itemsOnRack(models.Model):


    itemID = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    rack = models.CharField(max_length=500,default="*")
