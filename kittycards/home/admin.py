from django.contrib import admin
from .models import Profile, Card, Listing, Bid

# Register your models here.
admin.site.register(Profile)
admin.site.register(Card)
admin.site.register(Listing)
admin.site.register(Bid)