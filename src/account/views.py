from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

def login_signup_view(request):
    if request.method == 'POST':
        next_url = request.POST.get('next', '/')

        # Validate the next_url to avoid open redirect vulnerabilities
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            next_url = '/'

        if 'logout-form' in request.POST:
            logout(request)
            return redirect('home')

        if 'login-signup-form' in request.POST:
            username = request.POST.get('login-signup-form')
            if username is None or username.strip() == '':
                return render(request, 'home.html', {'error': 'Username cannot be empty.'})
            else:
                user = authenticate(request, username=username, password='')
                if user is not None:
                    login(request, user)
                    return redirect(next_url)
                else:
                    user = User.objects.create_user(username=username, password='')
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect(next_url)

    return render(request, 'home.html')
