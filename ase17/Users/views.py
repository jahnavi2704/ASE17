from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, redirect
from django.contrib.auth import  authenticate, login
from Users.forms import  RegistrationForm, ProfileRegistrationForm,ProfileUpdateForm
from .models import *
from Auctions.urls import *
from ase17.urls import *
from django.urls import reverse
# Create your views here.
def register(request):


    if request.method == 'POST':

        uf = RegistrationForm(request.POST, prefix='user')
        upf = ProfileRegistrationForm(request.POST, request.FILES, prefix='userprofile')

        if uf.is_valid() and upf.is_valid():
            password = uf.cleaned_data['confirm_password']
            user = uf.save(commit=False)
            user.set_password(password)
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.user = user
            userprofile.save()
            login(request, user)
            return redirect('dashboard')
    else:

        uf = RegistrationForm(prefix='user')
        upf = ProfileRegistrationForm(prefix='userprofile')
    context = {'userform': uf, 'userprofileform': upf}
    return render(request, 'registration/register.html', context)

@login_required(login_url='login')
def UpdateProfile(request):

    

    if request.method == 'POST':


        puf = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        print(puf.fields)
        if puf.is_valid():

            puf.save()
            context = {'message':'You Have Updated Your Profile Successfully'}
            print(context)
            return redirect('dashboard')

        else:
            context = {'message':'There Was Some Error'}
            print(context)

    else:

        puf = ProfileUpdateForm(instance=request.user.profile)
        context = {'ProfileUpdateForm': puf}
        return render(request, 'Users/ProfileUpdate.html', context)



