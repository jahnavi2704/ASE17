from django.urls import path, include
from Auctions import views

urlpatterns = [

    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('create-auction/', views.create_auction, name = 'create-auction'),
    path('auctions/<str:category>',views.display_auction , name='display-auction'),
    path('auctions/<str:category>/<int:itemset_id>',views.display_items, name='display-items'),
    path('tdashboard/',views.tdashboard),
    path('search/', views.search_by_keywords,name='search'),
    path('join/<int:auction_id>',views.join_auction,name='join'),
    path('dashboard/created-auctions/', views.view_created, name = 'view-created'),
    path('dashboard/participated-auctions/', views.view_participating, name= 'view-joined'),
    path('about/', views.about, name='about'),
    path('policies/', views.policy, name='policy'),
    
]
