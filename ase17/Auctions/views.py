from django.shortcuts import render, redirect
from django.http import HttpResponse
from Users.views import *
from Auctions.forms import *
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from Auctions.models import *
from RestAuctionPortal.models import *


# Create your views here.

def index(request):
    return render(request, 'Auctions/home.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'Auctions/dashboard.html')


OPTIONS = {
    '1': 'Electronics',
    '2': 'Automobiles',
    '3': 'Fashion',
    '4': 'Sports',
    '5': 'Art',
    '6': 'Books',
    '7': 'Furniture',
    '8': 'Antiques',
    '9': 'Musical Equipment',
    '10': 'Industrial Equipment',
    '11': 'Gaming',
    '12': 'Stationary',
    '13': 'Industrial Equipment',
    '14': 'Gaming',
    '15': 'Jewellery',
    '16': 'Miscellaneous',
}


def create_keywords_table(auction_id):

    auction_object = Auction.objects.get(id=auction_id)
    itemset_object = auction_object.itemset
    itemlist = itemset_object.item_set.all()

    

    for item in itemlist:
        keywords_list = item.keywords.split(' ')
        for single_key in keywords_list:
            KeywordsTable.objects.create(Item=item,key=single_key)


@login_required(login_url='login')
def create_auction(request):
    auction_details = AuctionCreationForm()
    auction_formset = formset_factory(ItemDetailsForm)
    auction_formset_post = auction_formset(request.POST or None)
    if request.method == 'POST':

        auction_details = AuctionCreationForm(request.POST)
        auction_formset_post = auction_formset(request.POST, request.FILES)

        if auction_details.is_valid() and auction_formset_post.is_valid():

            details = auction_details.save(commit=False)
            details.category = OPTIONS[auction_details.cleaned_data.get('category')]
            details.creator = request.user.profile
            details.save()

            itemList = ItemSet.objects.create(ItemList=details)

            for item in auction_formset_post:
                item_name = item.cleaned_data.get('item_name')
                description = item.cleaned_data.get('description')
                base_price = item.cleaned_data.get('base_price')
                keywords = item.cleaned_data.get('keywords')

                keywords_list = keywords.split(',')
                keywords = ' '.join(keywords_list)

                # for single_keyword in keywords:
                #     KeywordsTable.objects.create(key=single_keyword,Item=item)

                item_instance = item.save(commit=False)
                item_instance.item = itemList
                item_instance.description = description
                item_instance.item_name = item_name
                item_instance.keywords = keywords
                item_instance.base_price = base_price
                item_instance.save()

            auction_details_entry = Test.objects.create(userprofile=request.user.profile,
                                            auctionid=details.id)

            create_keywords_table(details.id)            

            return redirect('dashboard')

        else:
            context = {'auction_details': auction_details,
                       'auction_formset': auction_formset_post}
            return render(request, 'Auctions/createAuction.html', context)

    context = {'auction_details': auction_details, 'auction_formset': auction_formset}
    return render(request, 'Auctions/createAuction.html', context)


def display_auction(request, category):
    # Auctions = Auction.objects.all()
    Auctions = Auction.objects.filter(category=category)
    context = {}

    if not bool(Auctions):
        context = {'message': 'Sorry No Auctions Right Now !!'}
    else:
        context['query_set'] = Auctions

    context['category'] = category
    return render(request, 'Auctions/categories.html', context)


def display_items(request, category, itemset_id):
    # items = itemset.item_set.all()
    itemset_object = ItemSet.objects.get(id=itemset_id)
    items = itemset_object.item_set.all()
    context = {'items': items}
    return render(request, 'Auctions/Items.html', context)


def tdashboard(request):
    print(request.user.profile.display_pic.url)
    return render(request, 'Auctions/tdashboard.html')


def Arrange(search_result):
    return len(search_result['matches'])


def search_by_keywords(request):


    context = {}

    query = request.GET['query']
    query = query.split(',')
    q=0
    while q < len(query):
        query[q] = query[q].strip()
        q+=1

    print(query)

    all_items = Item.objects.all()

    search_result = []

    for single_item in all_items:
        keywords = single_item.keywords
        matches = []
        print(single_item,'\n')
        print(single_item.keywords,'\n')
        for single_query in query:
            print(single_query)
            if single_query in keywords:
                matches.append(single_query)

        if not bool(matches):
            continue
        else:
            result = {'item': single_item, 'matches': matches}
            search_result.append(result)

    if not bool(search_result):
        message = 'Sorry No Items Found !!'
        context['message'] = message
    else:
        search_result.sort(key=Arrange, reverse=True)
        context['search_result'] = search_result


    for k in search_result :
        k['item_name'] = k['item'].item_name
        k['item_url'] = k['item'].item_pic.url
        k['item_price'] = k['item'].base_price
        k['item_description'] = k['item'].description
        k.pop('item',None)


    return render(request, 'Auctions/search.html', context)

@login_required(login_url='login')
def join_auction(request, auction_id):
    context = {}
    auction_object = Auction.objects.get(id=auction_id)
    bidder = request.user.profile
    creator = auction_object.creator

    if creator != request.user.profile:
        print(request.user.profile)
        print(bool(AuctionBidders.objects.filter(auction=auction_object, bidders=bidder).exists()))
        if not bool(AuctionBidders.objects.filter(auction=auction_object, bidders=bidder).exists()):

             AuctionBiddersInstance = AuctionBidders.objects.create(auction=auction_object, bidders=bidder)
             context = {'message': 'Joined Auction Successfully'}
    else:
         message = 'You Have Already Joined This Auction !!'
         context = {'message': message}
    print(context)
    return redirect('view-joined')

@login_required(login_url='login')
def dashboard(request):
    uname = request.user.id
    posts = Profile.objects.get(user=uname)
    context = {}
    context['posts'] = posts
    context['user'] = request.user
    return render(request, 'Auctions/profile.html', context)

@login_required(login_url='login')
def view_created(request):
    uname = request.user.profile
    #print(request.user.profile)
    auctions = Auction.objects.all().filter(creator=uname)
    context = {'auctions': auctions, 'options': OPTIONS}
    return render(request, 'Auctions/createdAuctionsDash.html', context)

@login_required(login_url='login')
def view_participating(request):
    uname = request.user.profile
    auction_bidder_instance = AuctionBidders.objects.all().filter(bidders=uname)

    view_participating = []

    for auction_bidder in auction_bidder_instance:
        view_participating.append({'auction': auction_bidder.auction, 'bidders': auction_bidder.bidders, 'creator': auction_bidder.auction.creator, 'scheduled_time': auction_bidder.auction.scheduled_date})


    context = {'view_participating':view_participating}
    return render(request, 'Auctions/joinedAuctionsDash.html', context)



    context = {'view_participating':view_participating}
    return render(request, 'Auctions/joinedAuctionsDash.html', context)

def about(request):
    return render(request, 'Auctions/about.html')

def policy(request):
    return render(request, 'Auctions/policies.html')
