from django import forms
from Auctions.models import *

class AuctionCreationForm(forms.ModelForm):

    class Meta:
        model = Auction
        exclude = ['creator']


class ItemDetailsForm(forms.ModelForm):

    class Meta:
        model = Item
        #exclude = ['bidder','updated_price','status','item']
        fields = ['item_name','base_price','description','keywords', 'item_pic']
        widgets = {
            'item_name': forms.TextInput(attrs={'required': True}),
            'base_price': forms.TextInput(attrs={'required': True}),
            'description': forms.TextInput(attrs={'required': True}),
            'keywords':forms.TextInput(attrs={'required': True}),
        }
    def clean(self):

        cleaned_data = super().clean()
        keywords = cleaned_data.get('keywords')

        if keywords :
            if len(keywords.split(',') ) == 1:
                self.add_error('keywords','Enter More Than 1 Keyword')



