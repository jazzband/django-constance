from django.db import models


class Shelf(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        verbose_name_plural = 'shelves'


class Supply(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        verbose_name_plural = 'supplies'
