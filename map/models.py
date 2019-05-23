from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Place(models.Model):
    address = models.CharField(max_length=200)
    coordinate_x = models.FloatField()
    coordinate_y = models.FloatField()
    type_mask = models.IntegerField()

    # Маска
    PLAST = 1
    PAPER = 2
    GLASS = 4
    ACCUM = 8
    TYPES = [PLAST, PAPER, GLASS, ACCUM]

    def __str__(self):
        return self.address + ':: ' + str((self.coordinate_x, self.coordinate_y))


class Proposal(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)

    # for admins only
    status = models.BooleanField(null=True)
    # enabled if status approved/disapproved
    status_explanation = models.TextField(max_length=300)

    def __str__(self):
        return self.author.username + ' предлагает изменить место #' + str(self.place.id) \
               + '. Изменения: ' + self.text[:20] + '...'
