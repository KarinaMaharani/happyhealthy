from django.shortcuts import render


def landing(request):
    """Landing page with login/register/guest options"""
    # Redirect to home if already logged in or guest
    if request.user.is_authenticated or request.session.get('is_guest'):
        return render(request, 'main/home.html')
    return render(request, 'main/landing.html')


def home(request):
    return render(request, 'main/home.html')


def about(request):
    context = {
        'page_title': 'About',
        'features': [
            {'icon': '🔍', 'title': 'Drug Search', 'desc': 'Search comprehensive drug database'},
            {'icon': '⚠️', 'title': 'Interaction Check', 'desc': 'Check drug-drug interactions'},
            {'icon': '📋', 'title': 'Detailed Info', 'desc': 'View complete drug information'},
            {'icon': '💾', 'title': 'Save Favorites', 'desc': 'Bookmark frequently used drugs'},
        ]
    }
    return render(request, 'main/about.html', context)
