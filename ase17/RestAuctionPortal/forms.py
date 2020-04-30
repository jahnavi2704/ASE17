from django import forms
from RestAuctionPortal.models import *

class TestForm(forms.Form):
    bid = forms.IntegerField(initial=0)
    
