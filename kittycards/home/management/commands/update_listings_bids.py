from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile, Listing, Bid
import datetime

class Command(BaseCommand):
    help = 'Background process for updating bids and listings in real-time'

    def handle(self, *args, **options):
        # first get all active listings,
        # then get most recent bid placed,
        # if current time > time updated for most recent bid + period:
        # change card belonging and set listing end time

        # sets deals
        listings = Listing.objects.filter(end_time=None)
        for listing in listings:
            bids = Bid.objects.filter(listing=listing, last_updated__gte=listing.start_time)
            if bids:
                bid_latest = bids.latest('last_updated')
                utc_dt = datetime.datetime.utcnow()
                now = utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
                # deal
                if bid_latest.last_updated + datetime.timedelta(0, 300) < now:
                    # receives money
                    lister_profile = Profile.objects.get(owner=listing.lister)
                    lister_profile.coins += bid_latest.price
                    lister_profile.save()
                    # pays money
                    bidder_profile = Profile.objects.get(owner=bid_latest.bidder)
                    bidder_profile.coins -= bid_latest.price
                    bidder_profile.save()
                    # card changes owner
                    card = listing.card
                    card.owner = bid_latest.bidder
                    card.save()
                    # listing ends
                    listing.end_time = now
                    listing.save()
                    self.stdout.write(self.style.SUCCESS('Updated listing "%s"' % listing.id))
            self.stdout.write(self.style.SUCCESS('Processed listing "%s"' % listing.id))
        # update coins withholded
        users_coins_withholded = {}
        for listing in listings:
            bids = Bid.objects.filter(listing=listing, last_updated__gte=listing.start_time)
            if bids:
                bid_latest = bids.latest('last_updated')
                user_id = bid_latest.bidder.id
                if not user_id in users_coins_withholded:
                    users_coins_withholded[user_id] = bid_latest.price
                else:
                    users_coins_withholded[user_id] += bid_latest.price
        for user in User.objects.all():
            profile = Profile.objects.get(owner=user)
            if user.id in users_coins_withholded:
                profile.coins_withholded = users_coins_withholded[user.id]
                self.stdout.write(self.style.SUCCESS('Added coins withholded for user "%s"' % user.id))
            else:
                profile.coins_withholded = 0
                self.stdout.write(self.style.SUCCESS('Resetted coins withholded for user "%s"' % user.id))
            profile.save()


