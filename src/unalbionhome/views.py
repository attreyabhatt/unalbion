from django.shortcuts import render


def home_view(request, *args, **kwargs):
    context = {
        'title': 'UnAlbion Home',
        'description': 'Welcome to UnAlbion, your go-to place for all things Albion Online.',
        'keywords': 'Albion Online, MMORPG, gaming, community',
    }
    return render(request, 'home.html', context)



    