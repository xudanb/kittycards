from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.db.models import Q
import datetime
from home.models import Profile, Card, Listing, Bid

# Create your views here.
class MainView(LoginRequiredMixin, View):
    template_name = 'bid/main.html'

    def get(self, request):
        # for every listing with end time null, get most recent bid placed after start_time (done)
        # if bid time - curr time > 5 mins, set listing end time, set listing card owner to bidder
        user_listings = Listing.objects.filter(lister=request.user, end_time=None)
        other_listings = Listing.objects.filter(~Q(lister=request.user), end_time=None)

        user_listings_bids = []
        for user_listing in user_listings:
            # find bid, add to list
            bid_latest = None
            bids = Bid.objects.filter(listing=user_listing, last_updated__gte=user_listing.start_time)
            if bids:
                bid_latest = bids.latest('last_updated')
            user_listings_bids.append({'user_listing':user_listing, 'bid_latest':bid_latest})

        other_listings_bids = []
        for other_listing in other_listings:
            if other_listing.lister.username!='deleted':
                # find bid, add to list
                bid_latest = None
                bids = Bid.objects.filter(listing=other_listing, last_updated__gte=other_listing.start_time)
                if bids:
                    bid_latest = bids.latest('last_updated')
                other_listings_bids.append({'other_listing':other_listing, 'bid_latest':bid_latest})

        # get current user's cards and all listings
        ctx = {
            'coins': Profile.objects.get(owner=request.user).coins,
            'coins_withholded': Profile.objects.get(owner=request.user).coins_withholded,
            'cards': Card.objects.filter(owner=request.user),
            'user_listings_bids': user_listings_bids,
            'other_listings_bids': other_listings_bids,
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        # if click to activate, set card owner to null, create listing with corresponding info (done)
        # if click to deactivate, set listing end time, set card owner to current user (done)
        card_id = request.POST.get('card_id')
        user_listing_id = request.POST.get('user_listing_id')
        other_listing_id = request.POST.get('other_listing_id')
        other_listing_id = request.POST.get('other_listing_id')
        if card_id:
            card = Card.objects.get(id=card_id)
            if card.owner == request.user:
                card.owner = None
                card.save()
                listing = Listing(card=card, lister=request.user)
                listing.save()
        elif user_listing_id:
            user_listing = Listing.objects.get(id=user_listing_id)
            if user_listing.lister == request.user and user_listing.end_time == None:
                user_listing.end_time = datetime.datetime.now()
                user_listing.card.owner = request.user
                user_listing.card.save()
                user_listing.save()
        elif other_listing_id:
            other_listing = Listing.objects.get(id=other_listing_id)
            if other_listing.lister != request.user and other_listing.end_time == None:
                # get added price
                addprice = request.POST.get('addprice')
                if addprice:
                    if addprice=="1":
                        added_price = 1
                    elif addprice=="2":
                        added_price = 10
                    elif addprice=="3":
                        added_price = 100
                    # find most recent bid, check if belong to user
                    bid_latest = None
                    bids = Bid.objects.filter(listing=other_listing, last_updated__gte=other_listing.start_time)
                    if bids:
                        bid_latest = bids.latest('last_updated')
                    current_price = 0
                    if bid_latest:
                        current_price = bid_latest.price
                    # check whether user can afford item
                    user_profile = Profile.objects.get(owner=request.user)
                    if user_profile.coins-user_profile.coins_withholded-added_price-current_price >= 0:
                        bid = Bid(listing=other_listing, bidder=request.user, price=added_price+current_price)
                        bid.save()
        return redirect('/bid')


