from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def login_signup_view(request):
    if request.method == 'POST':
        if 'logout-form' in request.POST:
            logout(request)
            return redirect('home')

        if 'login-signup-form' in request.POST:
            username = request.POST.get('login-signup-form')
            user = authenticate(request, username=username, password='')
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your home page
            else:
                return render(request, 'home.html', {'error': 'Invalid username'})
    return render(request, 'home.html')