 

# dappx/views.py
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from dappx.forms import UserForm,UserProfileInfoForm
from django.contrib.auth.decorators import login_required
''' views.py is for getting HTTP request and sending HTTP response'''
import dappx.AntiPhishing as AP
import numpy as np
import pickle

def sigmoid(z):
    z = np.float64(z)
    return 1.0/(1.0+np.exp(-1.0 * z))

def home(request):
    if request.method == 'POST':
        inpURL = request.POST['url']
        print(inpURL)
        features = AP.extractFeatures(inpURL,0)
        features = features[1:-1]
        a = np.array(features)
        a = a.reshape(11,1)
        f = open('dappx/trained.obj','rb')
        sizes = pickle.load(f)
        weights = pickle.load(f)
        biases = pickle.load(f)
        for b,w in zip(biases,weights):
            a = sigmoid(np.dot(w, a)+b)
        result = np.argmax(a)

        if(result == 1):
            return render(request,'dappx/danger.html',{'url':inpURL})      
        else:
            return redirect(inpURL)
    return render(request,'dappx/home.html')         
    


def special(request):
    return render(request,'dappx/base.html')
@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'dappx/signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'dappx/login.html', {})