from django.urls import path, include
from RestAuctionPortal import views

urlpatterns = [
    path('auction-portal/<int:auction_id>/',views.testform,name='testform'),

]