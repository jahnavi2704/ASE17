from django.db import models
from django.contrib.auth.models import  User
from Users.models import *
from Auctions.models import *

# Create your models here.

class SoldItemsData(models.Model):
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    bidder = models.ForeignKey(Profile,on_delete=models.CASCADE)
    WinningBid = models.IntegerField(default=0)

    def __str__(self):
        return f'Winning Bid Is {self.WinningBid} & sold to {self.bidder}'

class Test(models.Model):
    auctionid = models.IntegerField(default=0)
    current_item_no = models.IntegerField(default=0)
    time_reset = models.BooleanField(default=False)
    bid_increment = models.IntegerField(default=0)
    userprofile = models.ForeignKey(Profile,default=None,on_delete=models.DO_NOTHING)
    current_bid = models.IntegerField(default=0)