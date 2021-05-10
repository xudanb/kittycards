from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Card, Listing, Bid
import datetime

# Create your tests here.
class CreateTest(TestCase):
    def setUp(self):
        # initialize first user
        user1 = User.objects.create_user('user1', '', 'kittycards')
        profile1 = Profile.objects.create(owner=user1)
        # initialize card
        card = Card.objects.create(level=1, image='', owner=user1)
        # initialize listing
        listing = Listing.objects.create(start_time=datetime.datetime.now(), end_time=None, card=card, lister=user1)
        # initialize second user
        user2 = User.objects.create_user('user2', '', 'kittycards')
        profile2 = Profile.objects.create(owner=user2)
        # initialize bid
        bid = Bid.objects.create(last_updated=datetime.datetime.now(), listing=listing, bidder=user2)

    def test(self):
        # test users
        user1 = User.objects.get(username='user1')
        profile1 = Profile.objects.get(owner=user1)
        self.assertEqual(profile1.first_time, True)
        self.assertEqual(profile1.coins, 1000)
        self.assertEqual(profile1.coins_withholded, 0)
        user2 = User.objects.get(username='user2')
        profile2 = Profile.objects.get(owner=user2)
        self.assertEqual(profile2.first_time, True)
        self.assertEqual(profile2.coins, 1000)
        self.assertEqual(profile2.coins_withholded, 0)
        # test card
        card = Card.objects.get(owner=user1)
        self.assertEqual(card.level, 1)
        self.assertEqual(card.image, '')
        # test listing
        listings = Listing.objects.filter(lister=user1)
        self.assertEqual(len(listings), 1)
        listing = listings[0]
        self.assertIsNone(listing.end_time)
        # test bid
        bids = Bid.objects.filter(bidder=user2)
        self.assertEqual(len(bids), 1)
        bid = bids[0]
        self.assertEqual(bid.price, 0)
        # test listing and bid times
        self.assertGreaterEqual(bid.last_updated, listing.start_time)

# Create your tests here.
class UpdateTest(TestCase):
    def setUp(self):
        # initialize first user
        user1 = User.objects.create_user('user1', '', 'kittycards')
        profile1 = Profile.objects.create(owner=user1)
        # initialize card
        card = Card.objects.create(level=1, image='', owner=user1)
        # initialize listing
        listing = Listing.objects.create(start_time=datetime.datetime.now(), end_time=None, card=card, lister=user1)
        # initialize second user
        user2 = User.objects.create_user('user2', '', 'kittycards')
        profile2 = Profile.objects.create(owner=user2)
        # initialize bid
        bid = Bid.objects.create(last_updated=datetime.datetime.now(), listing=listing, bidder=user2)
        # update profiles
        user1 = User.objects.get(username='user1')
        profile1 = Profile.objects.get(owner=user1)
        profile1.coins += 100
        profile1.save()
        user2 = User.objects.get(username='user2')
        profile2 = Profile.objects.get(owner=user2)
        profile2.coins_withholded += 100
        profile2.save()
        # update card
        card = Card.objects.get(owner=user1)
        card.level = 3
        card.save()
        # update bid
        bids = Bid.objects.filter(bidder=user2)
        bid = bids[0]
        bid.last_updated = datetime.datetime.now()
        bid.save()
        # update listing
        listings = Listing.objects.filter(lister=user1)
        listing = listings[0]
        listing.end_time = datetime.datetime.now()
        listing.save()

    def test(self):
        # test profiles
        user1 = User.objects.get(username='user1')
        profile1 = Profile.objects.get(owner=user1)
        self.assertEqual(profile1.coins, 1100)
        user2 = User.objects.get(username='user2')
        profile2 = Profile.objects.get(owner=user2)
        self.assertEqual(profile2.coins_withholded, 100)
        # test card
        card = Card.objects.get(owner=user1)
        self.assertEqual(card.level, 3)
        # test listing
        listings = Listing.objects.filter(lister=user1)
        listing = listings[0]
        self.assertIsNotNone(listing.end_time)
        # test listing and bid times
        bids = Bid.objects.filter(bidder=user2)
        bid = bids[0]
        self.assertGreaterEqual(listing.end_time, bid.last_updated)

class DeleteTest1(TestCase):
    def setUp(self):
        # initialize first user
        user1 = User.objects.create_user('user1', '', 'kittycards')
        profile1 = Profile.objects.create(owner=user1)
        # initialize card
        card = Card.objects.create(level=1, image='', owner=user1)
        # initialize listing
        listing = Listing.objects.create(start_time=datetime.datetime.now(), end_time=None, card=card, lister=user1)
        # initialize second user
        user2 = User.objects.create_user('user2', '', 'kittycards')
        profile2 = Profile.objects.create(owner=user2)
        # initialize bid
        bid = Bid.objects.create(last_updated=datetime.datetime.now(), listing=listing, bidder=user2)
        user1.delete()

    def test(self):
        # test profiles
        profiles = Profile.objects.all()
        self.assertEqual(len(profiles), 1)
        profile2 = profiles[0]
        self.assertEqual(profile2.owner.username, 'user2')
        # test listing
        listings = Listing.objects.all()
        self.assertEqual(len(listings), 1)
        listing = listings[0]
        self.assertEqual(listing.lister.username, 'deleted')
        # test card
        card = listing.card
        self.assertEqual(card.owner.username, 'deleted')

class DeleteTest2(TestCase):
    def setUp(self):
        # initialize first user
        user1 = User.objects.create_user('user1', '', 'kittycards')
        profile1 = Profile.objects.create(owner=user1)
        # initialize card
        card = Card.objects.create(level=1, image='', owner=user1)
        # initialize listing
        listing = Listing.objects.create(start_time=datetime.datetime.now(), end_time=None, card=card, lister=user1)
        # initialize second user
        user2 = User.objects.create_user('user2', '', 'kittycards')
        profile2 = Profile.objects.create(owner=user2)
        # initialize bid
        bid = Bid.objects.create(last_updated=datetime.datetime.now(), listing=listing, bidder=user2)
        user2.delete()

    def test(self):
        # test profiles
        profiles = Profile.objects.all()
        self.assertEqual(len(profiles), 1)
        profile1 = profiles[0]
        self.assertEqual(profile1.owner.username, 'user1')
        # test listing
        bids = Bid.objects.all()
        self.assertEqual(len(bids), 1)
        bid = bids[0]
        self.assertEqual(bid.bidder.username, 'deleted')