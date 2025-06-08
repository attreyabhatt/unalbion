from django.db import models
from django.contrib.auth.models import User

class FishingBaitData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    worm_price = models.PositiveIntegerField()  # required
    t1_price = models.PositiveIntegerField(null=True, blank=True)
    t3_price = models.PositiveIntegerField(null=True, blank=True)
    t5_price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Fishing Input"
