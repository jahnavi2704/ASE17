from django.db import models
from Users.models import Profile,User
# Create your models here.

class Auction(models.Model):

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()

    OPTIONS = (
        ('1', 'Electronics'),
        ('2', 'Automobiles'),
        ('3', 'Fashion'),
        ('4', 'Sports'),
        ('5', 'Art'),
        ('6', 'Books'),
        ('7', 'Furniture'),
        ('8', 'Antiques'),
        ('9', 'Musical Equipment'),
        ('10', 'Industrial Equipment'),
        ('11', 'Gaming'),
        ('12', 'Stationary'),
        ('13', 'Utensils'),
        ('14', 'Precious Gems'),
        ('15', 'Pet Stuff'),
        ('16', 'Miscellaneous'),
    )

    category = models.CharField(max_length=200, choices=OPTIONS)


    def __str__(self):
        return f'Auction - {self.id}'

class AuctionBidders(models.Model):

    auction = models.ForeignKey(Auction,on_delete=models.CASCADE,null=True)
    bidders = models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return f'Auction Bidders - {self.auction},{self.bidders}'



class ItemSet(models.Model):
    ItemList = models.OneToOneField(Auction,on_delete=models.CASCADE)

    def __str__(self):
        return f'ItemSet - {self.id}'


class Item(models.Model):

    item = models.ForeignKey(ItemSet, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=40,null=True)
    description = models.TextField()
    base_price = models.FloatField()
    keywords = models.CharField(max_length=255,blank=True)
    status = models.BooleanField(default=False)
    updated_price =  models.FloatField(default=0,blank=False)
    bidder = models.OneToOneField(Profile,on_delete=models.CASCADE,blank=True,null=True)
    item_pic = models.ImageField(default='no_image.png', upload_to='item_pics')

    def __str__(self):
        return self.item_name

class KeywordsTable(models.Model):
     Item = models.ForeignKey(Item,on_delete=models.CASCADE,default=None)
     key = models.CharField(max_length=50, null=False)