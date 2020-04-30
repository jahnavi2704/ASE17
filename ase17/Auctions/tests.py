from django.test import TestCase
from django.http import request
from Auctions.models import *
from Users.models import Profile, User
import datetime
from django.test import Client


class TestAuction(TestCase):

    def setUp(self):
        self.user_object = User(username='pavan', email='mail@gmail.com')
        self.user_object.set_password('testing321')
        self.user_object.save()
        self.createduser = Profile.objects.create(user=self.user_object, phone_no='1234567891', address='Sricity',
                                                  card_no='1234567891011121')
        #print(self.createduser)
        self.createauction = Auction.objects.create(creator=self.createduser, scheduled_date=datetime.datetime.today()+datetime.timedelta(days=2), category='Gaming')
        self.client = None

    def test_Auction(self):
        self.assertTrue(Auction.objects.filter(creator=Profile.objects.get(phone_no='1234567891')).exists())

class TestAuctionBidders(TestCase):

    def setUp(self):
        self.user_object = User(username='pavan', email='mail@gmail.com')
        self.user_object.set_password('testing321')
        self.user_object.save()
        self.user_object1 = User(username='pavan1', email='mail1@gmail.com')
        self.user_object1.set_password('testing321')
        self.user_object1.save()
        self.createduser = Profile.objects.create(user=self.user_object, phone_no='1234567891', address='Sricity',
                                                  card_no='1234567891011121')
        self.createduser1 = Profile.objects.create(user=self.user_object1, phone_no='1234567890', address='SriCity',
                                                  card_no='1234567891011190')
        self.createauction = Auction.objects.create(creator=self.createduser,
                                                    scheduled_date=datetime.datetime.today() + datetime.timedelta(
                                                        days=2), category='Gaming')
        self.bidder = AuctionBidders.objects.create(auction=self.createauction, bidders=self.createduser1)
        self.client = None

    def test_AuctionBidders(self):
        self.auction = self.createauction
        self.bidders = self.createduser1
        self.assertFalse(Auction.objects.filter(creator=Profile.objects.get(phone_no='1234567890')).exists())
        self.assertTrue(Auction.objects.filter(creator=Profile.objects.get(phone_no='1234567891')).exists())
        self.assertTrue(AuctionBidders.objects.filter(bidders=Profile.objects.get(phone_no='1234567890')).exists())
        # auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
        # bidders = models.ForeignKey(Profile, on_delete=models.CASCADE)

class TestItemset(TestCase):

    def setUp(self):
        self.user_object = User(username='pavan', email='mail@gmail.com')
        self.user_object.set_password('testing321')
        self.user_object.save()
        self.createduser = Profile.objects.create(user=self.user_object, phone_no='1234567891', address='Sricity',
                                                          card_no='1234567891011121')
        self.createauction = Auction.objects.create(creator=self.createduser, scheduled_date=datetime.datetime.today()+datetime.timedelta(days=2), category='Gaming')
        self.itemset_create = ItemSet.objects.create(ItemList=self.createauction)
        #print(self.itemset_create)
        #self.itemset = self.createauction
        self.client = None

    def test_Itemset(self):
        self.assertTrue(ItemSet.objects.filter(ItemList=self.createauction).exists())
        # self.itemset =
        # ItemList = models.OneToOneField(Auction, on_delete=models.CASCADE)

class TestItem(TestCase):

    def setUp(self):
        self.user_object = User(username='pavan', email='mail@gmail.com')
        self.user_object.set_password('testing321')
        self.user_object.save()
        self.createduser = Profile.objects.create(user=self.user_object, phone_no='1234567891', address='Sricity',
                                                      card_no='1234567891011121')
        self.createauction = Auction.objects.create(creator=self.createduser, scheduled_date=datetime.datetime.today()+datetime.timedelta(days=2), category='Gaming')
        self.itemset_create = ItemSet.objects.create(ItemList=self.createauction)
        self.items = Item.objects.create(item=self.itemset_create, item_name='stand', description='well polished',
                                         base_price=342, keywords='polished', )
        self.client = None

    def test_Item(self):
        self.assertTrue(Item.objects.filter(item_name='stand').exists())
        #self.assertTrue(ItemSet.objects.filter(item_name='umbrella').exists())
        self.assertTrue(ItemSet.objects.filter(item=self.items).exists())
        # item = models.ForeignKey(ItemSet, on_delete=models.CASCADE)
        # item_name = models.CharField(max_length=40, null=True)
        # description = models.TextField()
        # base_price = models.FloatField()
        # keywords = models.CharField(max_length=255)
        # status = models.BooleanField(default=False)
        # updated_price = models.FloatField(default=0, blank=False)
        # bidder = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)

# class Testurl(TestCase):
#
#     def setUp(self):
#         self.user_object = User(username='pavan', email='mail@gmail.com')
#         self.user_object.set_password('testing321')
#         self.user_object.save()
#         self.createduser = Profile.objects.create(user=self.user_object, phone_no='1234567891', address='Sricity',
#                                                               card_no='1234567891011121')
#         self.createauction = Auction.objects.create(creator=self.createduser, scheduled_date=datetime.datetime.today()+datetime.timedelta(days=2), category='Gaming')
#         self.itemset_create = ItemSet.objects.create(ItemList=self.createauction)
#         self.items = Item.objects.create(item=self.itemset_create, item_name='stand', description='well polished',
#                                                  base_price=342, keywords='polished', )
#         self.client = None
#
#         self.request = '/auctions/Gaming/'
#         self.client = Client()
#
#     def test_url(self):
#         response = self.client.get(self.request)
#         #print(response.status_code)
#         self.assertRedirects(response, expected_url=self.request)