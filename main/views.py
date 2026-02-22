from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


from main.models import About_Us_Hero, Hero_Section, Service, Team_Member, why_us





# -------------------------------  Index Page View ---------------------------------- #
def index(request):
    return render(request, 'main/index.html', {
        'hero_section': Hero_Section.objects.all(),
        'team_members': Team_Member.objects.all(),
        'services': Service.objects.all(),
    })




# -------------------------------  Contact Page View ---------------------------------- #
def contact(request):
    return render(request, 'main/contact.html')







# -------------------------------  About Page View ---------------------------------- #
def about(request):
    return render(request, 'main/about.html', {
        'why_us': why_us.objects.all(),
        'team_members': Team_Member.objects.all(),
        'about_hero': About_Us_Hero.objects.all()
    })






# -------------------------------  Services Section View ---------------------------------- #
def services(request):
    return render(request, 'main/services.html', {
        'hero_section': Hero_Section.objects.all(),
        'services': Service.objects.all()
    })
    
def service_page(request, service_id):
    service = Service.objects.get(pk=service_id)
    return render(request, 'main/service_page.html', {
        "service": service
    })







# -------------------------------  Login Page View ---------------------------------- #
def user_in(request):
    import time
    max_attempts = 5
    lockout_minutes = 1
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        mandatory_field = request.POST.get('mandatory_field', '')
        attempts = request.session.get('login_attempts', 0)
        lockout_time = request.session.get('login_lockout_time')
        now = time.time()
        if lockout_time:
            elapsed = now - lockout_time
            if elapsed < lockout_minutes * 60:
                remaining = int(lockout_minutes - (elapsed // 60))
                return render(request, 'main/user_in.html', {'error': f'Too many failed login attempts. Try again in {remaining} minutes.'})
            else:
                # Lockout expired, reset
                request.session['login_attempts'] = 0
                request.session['login_lockout_time'] = None
                attempts = 0
        if attempts >= max_attempts:
            request.session['login_lockout_time'] = now
            return render(request, 'main/user_in.html', {'error': f'Too many failed login attempts. Try again in {lockout_minutes} minutes.'})
        if mandatory_field:
            request.session['login_attempts'] = attempts + 1
            if request.session['login_attempts'] >= max_attempts:
                request.session['login_lockout_time'] = now
            return render(request, 'main/user_in.html', {'error': 'Login failed.'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['login_attempts'] = 0  # Reset on successful login
            request.session['login_lockout_time'] = None
            return redirect('main:user_dash')  # Redirect to homepage or dashboard
        else:
            request.session['login_attempts'] = attempts + 1
            if request.session['login_attempts'] >= max_attempts:
                request.session['login_lockout_time'] = now
            return render(request, 'main/user_in.html', {'error': 'Invalid username or password'})
    return render(request, 'main/user_in.html')




# -------------------------------  Login Page View ---------------------------------- #
@login_required
def user_dash(request):
    return render(request, 'main/user_dash.html', {
        'hero_section': Hero_Section.objects.all(),
        'team_members': Team_Member.objects.all(),
        'services': Service.objects.all(),
        'about_hero': About_Us_Hero.objects.all(),
        'why_us': why_us.objects.all(),
    })


