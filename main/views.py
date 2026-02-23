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





   
# -------------------------------  Edit Hero Section ---------------------------------- #
@login_required
def edit_hero(request, hero_id):
    import os
    from django.conf import settings
    hero = Hero_Section.objects.get(pk=hero_id)
    if request.method == 'POST':
        hero.hero_text_title = request.POST.get('hero_text_title')
        hero.hero_text_body = request.POST.get('hero_text_body')
        if 'hero_image' in request.FILES:
            # Delete old image file if it exists
            if hero.hero_image and hasattr(hero.hero_image, 'path'):
                old_image_path = hero.hero_image.path
                if os.path.isfile(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception:
                        pass
            hero.hero_image = request.FILES['hero_image']
        hero.save()
        return redirect('main:index')
    return render(request, 'main/edit_hero.html', {'hero': hero})




# -------------------------------  Edit Service Section ---------------------------------- #
@login_required
def edit_service(request, service_id):
    import os
    from django.conf import settings
    service = Service.objects.get(pk=service_id)
    if request.method == 'POST':
        service.service_title = request.POST.get('service_title')
        service.service_description = request.POST.get('service_description')
        if 'service_image' in request.FILES:
            # Delete old image file if it exists
            if service.service_image and hasattr(service.service_image, 'path'):
                old_image_path = service.service_image.path
                if os.path.isfile(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception:
                        pass
            service.service_image = request.FILES['service_image']
        if 'service_icon' in request.FILES:
            service.service_icon = request.FILES['service_icon']
        service.save()
        return redirect('main:service_page', service_id=service.id)
    return render(request, 'main/edit_service.html', {'service': service})



# -------------------------------  Edit About Us Hero Section ---------------------------------- #
@login_required
def edit_about_us_hero(request, about_hero_id):
    import os
    from django.conf import settings
    about_hero = About_Us_Hero.objects.get(pk=about_hero_id)
    if request.method == 'POST':
        about_hero.about_hero_text_title = request.POST.get('about_hero_text_title')
        about_hero.about_hero_text_body = request.POST.get('about_hero_text_body')
        if 'about_hero_image' in request.FILES:
            # Delete old image file if it exists
            if about_hero.about_hero_image and hasattr(about_hero.about_hero_image, 'path'):
                old_image_path = about_hero.about_hero_image.path
                if os.path.isfile(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception:
                        pass
            about_hero.about_hero_image = request.FILES['about_hero_image']
        about_hero.save()
        return redirect('main:about')
    return render(request, 'main/edit_about_us_hero.html', {'about_hero': about_hero})



# -------------------------------  Edit Admin Team Member Section ---------------------------------- #
def edit_admin_team_member(request, member_id):
    import os
    from django.conf import settings
    member = Team_Member.objects.get(pk=member_id)
    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.position = request.POST.get('position')
        if 'image' in request.FILES:
            # Delete old image file if it exists
            if member.image and hasattr(member.image, 'path'):
                old_image_path = member.image.path
                if os.path.isfile(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception:
                        pass
            member.image = request.FILES['image']
        member.instagram_url = request.POST.get('instagram_url')
        member.twitter_url = request.POST.get('twitter_url')
        member.linkedin_url = request.POST.get('linkedin_url')
        member.save()
        return redirect('main:user_dash')
    return render(request, 'main/edit_admin_team_member.html', {'member': member})



@login_required
def edit_admin_why_us(request, why_us_id):
    import os
    from django.conf import settings
    why = why_us.objects.get(pk=why_us_id)
    if request.method == 'POST':
        why.why_us_title = request.POST.get('why_us_title')
        why.why_us_desc = request.POST.get('why_us_desc')
        if 'why_us_icon' in request.FILES:
            # Delete old image file if it exists
            if why.why_us_icon and hasattr(why.why_us_icon, 'path'):
                old_image_path = why.why_us_icon.path
                if os.path.isfile(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception:
                        pass
            why.why_us_icon = request.FILES['why_us_icon']
        why.save()
        return redirect('main:user_dash')
    return render(request, 'main/edit_admin_why_us.html', {'why': why})
