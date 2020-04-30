from rest_framework import serializers
from RestAuctionPortal.models import *
from Users.models import *

class CurrentBidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ('current_bid',
                    'userprofile',
                      'current_item_no',
                       'time_reset',
                        'bid_increment'
                        )