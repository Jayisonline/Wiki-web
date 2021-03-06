from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout


# from .forms import OrderForm, CreateUserForm
# Create your views here.


def signup(request): 
    form = UserCreationForm();

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            # user = form.cleaned_data.get('username')
            # form.success(request, 'Account was created for '+ user)
            return redirect("login")

    return render(request, "encyclopedia/signup.html", {
        'form':form
    })


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('pswd')
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, username)
            return redirect("{{ index }}")
    context = {}
    return render(request, 'encyclopedia/login.html', context)
