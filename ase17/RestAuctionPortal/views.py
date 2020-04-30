from django.shortcuts import render, redirect
from RestAuctionPortal.forms import TestForm
from RestAuctionPortal.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from Auctions import urls
import json
from rest_framework import serializers


def calculate_bid_increment(bid):

    if bid in range(0,401):
        return 5
    if bid in range(1,401):
        return 5
    if bid in range(401,2001):
        return 20
    if bid in range(2001,7001):
        return 40
    if bid in range(7001,17501):
        return 100
    if bid in range(17501,35001):
        return 200
    if bid in range(35001,70001):
        return 300
    if bid in range(70001,175001):
        return 1000
    if bid in range(175001,350001):
        return 2000
    if bid in range(350001,700001):
        return 4000
    if bid > 700001 :
        return 10000


@csrf_exempt
def testform(request,auction_id):

    if request.method == 'GET':

        testform = TestForm()
        context = {}

        auction_object = Auction.objects.get(id=auction_id)
        itemset_object = auction_object.itemset
        itemlist = itemset_object.item_set.all()

        auction_item_list = itemlist.values('item_name','description','base_price')

        for j in range(len(auction_item_list)):
            auction_item_list[j]['item_url'] = str(itemlist[j].item_pic.url)

        clist = [i for i in auction_item_list]

        bid_instance = Test.objects.get(auctionid=auction_id)
        bid_instance.current_bid = clist[0]['base_price']
        bid_instance.save()

        context['itemlist'] = clist
        context['form'] = testform
        context['auction_id'] = auction_id
        return render(request,'RestAuctionPortal/auctionportal.html',context)

    if request.method == 'POST':

        data = JSONParser().parse(request)
        print(data)

        #postman
        if 'username' in data:
            print('postman request')
            up= data['username']
            userprofile=User.objects.get(username=up)
            userprofile=userprofile.profile

            current_bid_instance = Test.objects.get(auctionid=auction_id)
            timereset = True
            current_bid_instance.time_reset = timereset
            bid_increment = calculate_bid_increment(current_bid_instance.current_bid)
            current_bid_instance.bid_increment = bid_increment

            current_bid_instance.current_bid = int(current_bid_instance.current_bid) + int(bid_increment)

            current_bid_instance.save()

            serialized_testform = CurrentBidSerializer(current_bid_instance)
            return JsonResponse(serialized_testform.data)   

        #form django
        else:
            userprofile = request.user.profile

        #check time
        if 'time' in data:

            if data['time'] == 'reset':
                
                #get the item
                auction_object = Auction.objects.get(id=auction_id)
                itemset_object = auction_object.itemset
                itemlist = itemset_object.item_set.all()

                #get current bid details
                current_bid_instance = Test.objects.get(auctionid=auction_id)

                #select it
                item = itemlist[current_bid_instance.current_item_no]

                #save sold item details
                sold_item_data = SoldItemsData.objects.create( \
                        auction = auction_object,
                        bidder=userprofile,
                        item=item,
                        WinningBid = current_bid_instance.current_bid
                        )

                #get next item object
                item = itemlist[current_bid_instance.current_item_no + 1]

                #update running bid details 
                current_bid_instance.current_item_no = current_bid_instance.current_item_no+1
                current_bid_instance.userprofile = auction_object.creator
                current_bid_instance.time_reset = False
                current_bid_instance.current_bid = item.base_price
                bid_increment = calculate_bid_increment(current_bid_instance.current_bid)
                current_bid_instance.bid_increment = bid_increment

                #save it
                current_bid_instance.save()

                #return json serialized model
                serialized_testform = CurrentBidSerializer(current_bid_instance)
                return JsonResponse(serialized_testform.data)
            if data['time'] == 'theend':
                auction_object = Auction.objects.get(id=auction_id)
                itemset_object = auction_object.itemset
                itemlist = itemset_object.item_set.all()

                current_bid_instance = Test.objects.get(auctionid=auction_id)

                item = itemlist[current_bid_instance.current_item_no]

                sold_item_data = SoldItemsData.objects.create( \
                        auction = auction_object,
                        bidder=userprofile,
                        item=item,
                        WinningBid = current_bid_instance.current_bid
                        )
                json1 = {'end':'end'}
                return JsonResponse(json1)

        else:
            #update bid price
            current_bid_instance = Test.objects.get(auctionid=auction_id)
            bid = data['bid']
            timereset = False
            current_bid_instance.time_reset = timereset

            if int(bid) > int(current_bid_instance.current_bid):
                current_bid_instance.current_bid = int(bid)
                current_bid_instance.userprofile = userprofile
                current_bid_instance.time_reset = True
                current_bid_instance.save()

            bid_increment = calculate_bid_increment(int(bid))
            current_bid_instance.bid_increment = bid_increment

            current_bid_instance.save()

            serialized_testform = CurrentBidSerializer(current_bid_instance)
            return JsonResponse(serialized_testform.data)
