"""ase17 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from Users import views
from django.conf.urls.static import static
from django.conf import settings


#398281219081-ua806fjaae2v88m0gl6gajlhs22d56c0.apps.googleusercontent.com Client ID
#xCxnE7JeqKTsldx5HDrI0NdH Client Secret

admin.site.site_header = "BID_N_WIN"
admin.site.site_title = "BID_N_WIN"
admin.site.index_title = "BID_N_WIN"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Users.urls')),
    path('',include('Auctions.urls')),
    path('',include('RestAuctionPortal.urls')),
    path('accounts/',include('django.contrib.auth.urls'), name="accounts"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
