from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from member.forms import LoginForm
from django.contrib import messages

# Create your views here.
def loginView(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["u_name"]
            passwd = form.cleaned_data["u_passwd"]
            user = authenticate(username=user_name, password=passwd)
            if user is not None and (user.is_active or user.is_superuser):
                auth_login(request, user)
                if not User.objects.filter(username=user_name).exists():
                    messages.warning(request, "Vous n'existez pas")
                else:
                    messages.success(request, "Bravo")
                    return redirect('accueil')
               
        
            else:
                messages.warning(request, "Invalide")

    else:
        form = LoginForm()

    return render(request, 'member/login.html', locals())


def logoutView(request):
    auth_logout(request)
    return redirect(reverse(loginView))