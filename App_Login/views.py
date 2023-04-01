from urllib import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


from App_Login.forms import UserForm


# Create your views here.


def register(request):
    form = UserForm()
    if request.method == 'POST':
            form = UserForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account Created Successfully!")
                return HttpResponseRedirect(reverse('App_Login:register'))

    return render(request, 'App_Login/registration.html', context={'form':form})

def login_page(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Login:profile'))

    return render(request, 'App_Login/login.html', context={'form': form})


def home(request):
    return render(request, 'App_Login/profile.html')

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))
