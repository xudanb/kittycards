import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kittycards.settings")
django.setup()

from django.core import management
from home.management.commands import update_listings_bids
while True:
    management.call_command(update_listings_bids.Command())