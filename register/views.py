from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login

from .forms import UserLoginForm, UserRegisterForm
from .models import Accounts




def login_view(request):
    """Here we define the login view"""

    next = request.GET.get('next')
    form_register = UserRegisterForm(request.POST or None)
    form_loggin = UserLoginForm(request.POST or None)

    print("calling loggin views")

    if form_loggin.is_valid():

        username = form_loggin.cleaned_data.get('username')
        password = form_loggin.cleaned_data.get('password')

        print(username, password)

        
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')

    
    else:

        context = {'login': form_loggin, "register":form_register,
                   "error": "mail existing already", "mode":"login"}
        return render(request, "compte.html", context)



def register_view(request):
    """Here we define the register view"""

    next = request.GET.get('next')
    form_register = UserRegisterForm(request.POST or None)
    form_loggin = UserLoginForm(request.POST or None)

    if form_register.is_valid():

        user = form_register.save(commit=False)
        password = form_register.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        
        acc = Accounts(name=user.username)
        acc.save()
 
        new_user = authenticate(username=user.username, password=password)

        login(request, new_user)

        return redirect('/')

    else:


        context = {'login': form_loggin, "register":form_register,
                   "mode":"register"}
  
        return render(request, "compte.html", context)





def compte(request):


    form_login = UserLoginForm(request.POST or None)
    form_register = UserRegisterForm(request.POST or None)

    context = {'login': form_login, 'register': form_register}

    return render(request, "compte.html", context)









def logout_view(request):
    """Here we define logout session"""

    logout(request)
    print("déconnexion")
    return redirect('/')
