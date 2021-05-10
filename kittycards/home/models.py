from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class Profile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    first_time = models.BooleanField(default=True)
    coins = models.IntegerField(default=1000)
    coins_withholded = models.IntegerField(default=0)

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Card(models.Model):
    level = models.IntegerField() # 1, 2, 3 for bronze, silver, gold
    image = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))

class Listing(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    lister = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))

class Bid(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    price = models.IntegerField(default=0)