from django.contrib import admin
from Auctions.models import *

# Register your models here.

admin.site.register(Auction)
admin.site.register(ItemSet)
admin.site.register(Item)
admin.site.register(AuctionBidders)
admin.site.register(KeywordsTable)