from django.core.cache import cache
from datetime import datetime

def get_activity_time_with_cache():
    user_activity_time = None
    if 'user_activity_time' in cache:
        user_activity_time = cache.get('user_activity_time')
    else:
        user_activity_time = datetime.now().time()
        cache.set('user_activity_time', user_activity_time)
    return user_activity_time

def update_activity_time_with_cache():
    if 'user_activity_time' in cache:
        user_activity_time = datetime.now().time()
        cache.set('user_activity_time', user_activity_time)
        return user_activity_time
        
