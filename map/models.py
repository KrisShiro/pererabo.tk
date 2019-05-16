from django.db import models


# Create your models here.


class Place(models.Model):
    address = models.CharField(max_length=200)
    coordinate_x = models.FloatField()
    coordinate_y = models.FloatField()
    type_mask = models.IntegerField()

    PLAST = 1
    PAPER = 2
    GLASS = 4
    ACCUM = 8
    TYPES = [PLAST, PAPER, GLASS, ACCUM]

    def __str__(self):
        return self.address
