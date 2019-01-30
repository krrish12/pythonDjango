from django.shortcuts import render
from .cacheService import get_activity_time_with_cache

def index(request):
    get_activity_time_with_cache()
    return render(request, 'users/index.html')
