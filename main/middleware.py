import time
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = 600  # 10 minute (in seconds)

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = time.time()
            last_activity = request.session.get('last_activity')

            if last_activity:
                elapsed = current_time - last_activity
                if elapsed > self.timeout:
                    logout(request)
                    return redirect('main:user_in')  # redirect to login page

            # Update last activity time
            request.session['last_activity'] = current_time

        response = self.get_response(request)
        return response