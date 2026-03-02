from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

import os
from django.conf import settings

from django.core.exceptions import ValidationError
from django.contrib import messages



from main.models import About_Us_Hero, Contact_Us, Hero_Section, Service, Team_Member, why_us





# -------------------------------  Home Page Contents  ---------------------------------- #
def index(request):
    return render(request, 'main/index.html', {
        'hero_section': Hero_Section.objects.all(),
        'team_members': Team_Member.objects.order_by('?'),
        'services': Service.objects.order_by('?'),
    })





# -------------------------------  Contact Page Route  ---------------------------------- #
def contact(request):
    return render(request, 'main/contact.html', {
        'about_hero': About_Us_Hero.objects.all()
    })





# -------------------------------  About Page Contents ---------------------------------- #
def about(request):
    return render(request, 'main/about.html', {
        'why_us': why_us.objects.all(),
        'team_members': Team_Member.objects.all(),
        'about_hero': About_Us_Hero.objects.all()
    })





# -------------------------------  Services Page Contents ---------------------------------- #
def services(request):
    return render(request, 'main/services.html', {
        'hero_section': Hero_Section.objects.all(),
        'services': Service.objects.all()
    })





# -------------------------------  Individual Service View  ---------------------------------- #
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





# -------------------------------  Admin Dashboard Contents  ---------------------------------- #
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
    hero = Hero_Section.objects.get(pk=hero_id)
    
    if request.method == 'POST':
        hero.hero_text_title = request.POST.get('hero_text_title')
        hero.hero_text_body = request.POST.get('hero_text_body')
        validation_passed = True  # Flag to track if we can redirect

        if 'hero_image' in request.FILES:
            new_image = request.FILES['hero_image']
            # Validate image format
            valid_extensions = ['jpeg', 'jpg', 'png']
            extension = new_image.name.split('.')[-1].lower()
            
            if extension not in valid_extensions:
                messages.error(request, "Unsupported image format. Please upload JPEG, JPG, or PNG.")
                validation_passed = False
            else:
                # Delete old image if replacing
                if hero.hero_image and hasattr(hero.hero_image, 'path'):
                    hero.hero_image.delete(save=False)
                hero.hero_image = new_image
        
        if validation_passed:
            try:
                hero.full_clean()  # Validate all model fields
                hero.save()
                return redirect('main:index')  # Redirect on success
            except ValidationError as e:
                messages.error(request, f"Validation error: {e}")
    
    # If validation fails or GET request, remain on edit page
    return render(request, 'main/edit_hero.html', {'hero': hero})




# -------------------------------  Edit Service Section ---------------------------------- #
@login_required
def edit_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    
    if request.method == 'POST':
        service.service_title = request.POST.get('service_title')
        service.service_description = request.POST.get('service_description')
        mandatory_field = request.POST.get('mandatory_field', '')
        
        if mandatory_field:
            return redirect('main:logout')

        validation_passed = True
        temp_image = None
        temp_icon = None

        # Validate service_image (JPEG, JPG, PNG)
        if 'service_image' in request.FILES:
            new_image = request.FILES['service_image']
            valid_image_extensions = ['jpeg', 'jpg', 'png']
            extension = new_image.name.split('.')[-1].lower()
            
            if extension not in valid_image_extensions:
                messages.error(request, "Unsupported service image format. Upload JPEG, JPG, or PNG.")
                validation_passed = False
            else:
                temp_image = new_image  # Keep it temporarily

        # Validate service_icon (SVG only)
        if 'service_icon' in request.FILES:
            new_icon = request.FILES['service_icon']
            valid_icon_extensions = ['svg', 'png']
            extension = new_icon.name.split('.')[-1].lower()
            
            if extension not in valid_icon_extensions:
                messages.error(request, "Unsupported service icon format. Only SVG and PNG allowed.")
                validation_passed = False
            else:
                temp_icon = new_icon  # Keep it temporarily

        # Save only if all validations passed
        if validation_passed:
            try:
                service.full_clean()  # Validate all model fields

                # Assign new files only after validation
                if temp_image:
                    # Delete old image file safely
                    if service.service_image and hasattr(service.service_image, 'path'):
                        old_image_path = service.service_image.path
                        if os.path.isfile(old_image_path):
                            try:
                                os.remove(old_image_path)
                            except Exception:
                                pass
                    service.service_image = temp_image

                if temp_icon:
                    service.service_icon = temp_icon

                service.save()
                messages.success(request, "Service updated successfully!")
                return redirect('main:service_page', service_id=service.id)

            except ValidationError as e:
                messages.error(request, f"Validation error: {e}")

    # Stay on edit page if validation fails
    return render(request, 'main/edit_service.html', {'service': service})






# -------------------------------  Edit About Us Hero Section ---------------------------------- #
@login_required
def edit_about_us_hero(request, about_hero_id):
    about_hero = About_Us_Hero.objects.get(pk=about_hero_id)
    
    if request.method == 'POST':
        about_hero.about_hero_text_title = request.POST.get('about_hero_text_title')
        about_hero.about_hero_text_body = request.POST.get('about_hero_text_body')
        mandatory_field = request.POST.get('mandatory_field', '')
        
        if mandatory_field:
            return redirect('main:logout')

        validation_passed = True
        temp_image = None  # Hold uploaded image temporarily

        # Validate about_hero_image (JPEG, JPG, PNG)
        if 'about_hero_image' in request.FILES:
            new_image = request.FILES['about_hero_image']
            valid_extensions = ['jpeg', 'jpg', 'png']
            extension = new_image.name.split('.')[-1].lower()
            
            if extension not in valid_extensions:
                messages.error(request, "Unsupported image format. Upload JPEG, JPG, or PNG.")
                validation_passed = False
            else:
                temp_image = new_image  # Keep temporarily

        # Save only if all validations pass
        if validation_passed:
            try:
                about_hero.full_clean()  # Validate all model fields

                # Assign new image and safely delete old one
                if temp_image:
                    if about_hero.about_hero_image and hasattr(about_hero.about_hero_image, 'path'):
                        old_image_path = about_hero.about_hero_image.path
                        if os.path.isfile(old_image_path):
                            try:
                                os.remove(old_image_path)
                            except Exception:
                                pass
                    about_hero.about_hero_image = temp_image

                about_hero.save()
                messages.success(request, "About Us Hero updated successfully!")
                return redirect('main:about')

            except ValidationError as e:
                messages.error(request, f"Validation error: {e}")

    # Stay on edit page if validation fails
    return render(request, 'main/edit_about_us_hero.html', {'about_hero': about_hero})





# -------------------------------  Edit Admin Team Member Section ---------------------------------- #
@login_required
def edit_admin_team_member(request, member_id):
    member = Team_Member.objects.get(pk=member_id)

    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.position = request.POST.get('position')
        mandatory_field = request.POST.get('mandatory_field', '')
        
        if mandatory_field:
            return redirect('main:logout')

        validation_passed = True
        temp_image = None  # Temporary storage for new image

        # Validate uploaded image (JPEG, JPG, PNG)
        if 'image' in request.FILES:
            new_image = request.FILES['image']
            valid_extensions = ['jpeg', 'jpg', 'png']
            extension = new_image.name.split('.')[-1].lower()

            if extension not in valid_extensions:
                messages.error(request, "Unsupported image format. Upload JPEG, JPG, or PNG.")
                validation_passed = False
            else:
                temp_image = new_image  # Keep temporarily

        # Update social links
        member.instagram_url = request.POST.get('instagram_url')
        member.twitter_url = request.POST.get('twitter_url')
        member.linkedin_url = request.POST.get('linkedin_url')

        # Save only if validations passed
        if validation_passed:
            try:
                member.full_clean()  # Validate all model fields

                # Assign new image and safely delete old one
                if temp_image:
                    if member.image and hasattr(member.image, 'path'):
                        old_image_path = member.image.path
                        if os.path.isfile(old_image_path):
                            try:
                                os.remove(old_image_path)
                            except Exception:
                                pass
                    member.image = temp_image

                member.save()
                messages.success(request, "Team member updated successfully!")
                return redirect('main:user_dash')

            except ValidationError as e:
                messages.error(request, f"Validation error: {e}")

    # Stay on edit page if validation fails
    return render(request, 'main/edit_admin_team_member.html', {'member': member})








# -------------------------------  Eidt Admin Why Us Section View ---------------------------------- #
@login_required
def edit_admin_why_us(request, why_us_id):
    why = why_us.objects.get(pk=why_us_id)

    if request.method == 'POST':
        why.why_us_title = request.POST.get('why_us_title')
        why.why_us_desc = request.POST.get('why_us_desc')
        mandatory_field = request.POST.get('mandatory_field', '')
        
        if mandatory_field:
            return redirect('main:logout')

        validation_passed = True
        temp_icon = None  # Temporary storage for new icon

        # Validate why_us_icon (SVG only)
        if 'why_us_icon' in request.FILES:
            new_icon = request.FILES['why_us_icon']
            valid_extensions = ['svg', 'png']
            extension = new_icon.name.split('.')[-1].lower()

            if extension not in valid_extensions:
                messages.error(request, "Unsupported icon format. Only SVG and PNG allowed.")
                validation_passed = False
            else:
                temp_icon = new_icon  # Keep temporarily

        # Save only if validations passed
        if validation_passed:
            try:
                why.full_clean()  # Validate model fields

                # Assign new icon and safely delete old one
                if temp_icon:
                    if why.why_us_icon and hasattr(why.why_us_icon, 'path'):
                        old_image_path = why.why_us_icon.path
                        if os.path.isfile(old_image_path):
                            try:
                                os.remove(old_image_path)
                            except Exception:
                                pass
                    why.why_us_icon = temp_icon

                why.save()
                messages.success(request, "Why Us entry updated successfully!")
                return redirect('main:user_dash')

            except ValidationError as e:
                messages.error(request, f"Validation error: {e}")

    # Stay on edit page if validation fails
    return render(request, 'main/edit_admin_why_us.html', {'why': why})









# -------------------------------  Add New Service  ---------------------------------- #
@login_required
def add_new_service(request):
    if request.method == 'POST':
        service_title = request.POST.get('service_title')
        service_description = request.POST.get('service_description')
        service_image = request.FILES.get('service_image')
        service_icon = request.FILES.get('service_icon')
        mandatory_field = request.POST.get('mandatory_field', '')

        if mandatory_field:
            return redirect('main:logout')

        validation_passed = True

        # Validate service_image
        if service_image:
            ext = service_image.name.split('.')[-1].lower()
            if ext not in ['jpeg', 'jpg', 'png']:
                messages.error(request, "Service image must be JPEG, JPG, or PNG.")
                validation_passed = False

        # Validate service_icon
        if service_icon:
            ext = service_icon.name.split('.')[-1].lower()
            if ext not in ['svg', 'jpeg', 'jpg', 'png']:
                messages.error(request, "Service icon must be SVG, JPEG, or JPG.")
                validation_passed = False

        if validation_passed:
            try:
                new_service = Service(
                    service_title=service_title,
                    service_description=service_description,
                    service_image=service_image,
                    service_icon=service_icon,
                    mandatory_field=mandatory_field
                )
                new_service.full_clean()  # Run model-level validations
                new_service.save()
                messages.success(request, "New service added successfully!")
                return redirect('main:service_page', service_id=new_service.id)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

    return render(request, 'main/add_new_service.html')






# -------------------------------  Add New Team Member ---------------------------------- #
@login_required
def add_new_team_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        mandatory_field = request.POST.get('mandatory_field', '')
        if mandatory_field:
            return redirect('main:logout') 

        image = request.FILES.get('image')
        instagram_url = request.POST.get('instagram_url')
        twitter_url = request.POST.get('twitter_url')
        linkedin_url = request.POST.get('linkedin_url')

        validation_passed = True

        # Validate image
        if image:
            ext = image.name.split('.')[-1].lower()
            if ext not in ['jpeg', 'jpg', 'png']:
                messages.error(request, "Member image must be JPEG, JPG, or PNG.")
                validation_passed = False

        if validation_passed:
            try:
                # Create instance but don't save yet
                new_member = Team_Member(
                    name=name,
                    position=position,
                    image=image,
                    instagram_url=instagram_url,
                    twitter_url=twitter_url,
                    linkedin_url=linkedin_url,
                    mandatory_field=mandatory_field
                )
                new_member.full_clean()  # Validate model fields
                new_member.save()
                messages.success(request, "New team member added successfully!")
                return redirect('main:user_dash')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

    return render(request, 'main/add_new_team_member.html')





# -------------------------------  Add New Why Us ---------------------------------- #
@login_required
def add_new_why_us(request):
    if request.method == 'POST':
        why_us_title = request.POST.get('why_us_title')
        why_us_desc = request.POST.get('why_us_desc')
        mandatory_field = request.POST.get('mandatory_field', '')

        if mandatory_field:
            return redirect('main:logout')        

        why_us_icon = request.FILES.get('why_us_icon')
        validation_passed = True

        # Validate icon (PNG or SVG only)
        if why_us_icon:
            ext = why_us_icon.name.split('.')[-1].lower()
            if ext not in ['png', 'svg']:
                messages.error(request, "Why Us icon must be a PNG or SVG file.")
                validation_passed = False

        if validation_passed:
            try:
                # Create instance but don't save yet
                new_why = why_us(
                    why_us_title=why_us_title,
                    why_us_desc=why_us_desc,
                    why_us_icon=why_us_icon,
                    mandatory_field=mandatory_field
                )
                new_why.full_clean()  # Validate model fields
                new_why.save()
                messages.success(request, "New Why Us entry added successfully!")
                return redirect('main:user_dash')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

    return render(request, 'main/add_new_why_us.html')





# -------------------------------  Delete Service  ---------------------------------- #
@login_required
def delete_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    if service.service_image and hasattr(service.service_image, 'path'):
        image_path = service.service_image.path
        if os.path.isfile(image_path):
            try:
                os.remove(image_path)
            except Exception:
                pass
    if service.service_icon and hasattr(service.service_icon, 'path'):
        icon_path = service.service_icon.path
        if os.path.isfile(icon_path):
            try:
                os.remove(icon_path)
            except Exception:
                pass
    service.delete()
    return redirect('main:user_dash')






# -------------------------------  Delete Team Member  ---------------------------------- #
@login_required
def delete_team_member(request, member_id):
    member = Team_Member.objects.get(pk=member_id)
    if member.image and hasattr(member.image, 'path'):
        image_path = member.image.path
        if os.path.isfile(image_path):
            try:
                os.remove(image_path)
            except Exception:
                pass
    member.delete()
    return redirect('main:user_dash')






# -------------------------------  Delete Why Us  ---------------------------------- #
@login_required
def delete_why_us(request, why_us_id):
    why = why_us.objects.get(pk=why_us_id)
    if why.why_us_icon and hasattr(why.why_us_icon, 'path'):
        icon_path = why.why_us_icon.path
        if os.path.isfile(icon_path):
            try:
                os.remove(icon_path)
            except Exception:
                pass
    why.delete()
    return redirect('main:user_dash')





# -------------------------------  Logout Function  ---------------------------------- #
def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('main:index')





# -------------------------------  Contact Form Logic  ---------------------------------- #
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        message = request.POST.get('message')
        mandatory_field = request.POST.get('mandatory_field', '')

        # Anti-spam/mandatory field check
        if mandatory_field:
            return redirect('main:logout') 

        validation_passed = True

        # Basic field validation
        if not name:
            messages.error(request, "Name is required!")
            validation_passed = False
        if not email:
            messages.error(request, "Email is required!")
            validation_passed = False
        if not tel:
            messages.error(request, "Telephone number is required!")
            validation_passed = False
        if not message:
            messages.error(request, "Message is required!")
            validation_passed = False

        if validation_passed:
            try:
                # Create instance but don't save yet
                new_contact_message = Contact_Us(
                    name=name,
                    email=email,
                    tel=tel,
                    message=message,
                    mandatory_field=mandatory_field
                )
                new_contact_message.full_clean()  # Model-level validation
                new_contact_message.save()
                messages.success(request, "Your message has been sent successfully!")
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

    return render(request, 'main/contact.html')





# -------------------------------  Contact Form List Page  ---------------------------------- #
@login_required
def client_contact(request):
    return render(request, 'main/client_contact.html', {
        'client_contact': Contact_Us.objects.all().order_by('-id')
    })





# -------------------------------  Contact Form Message Detail Page  ---------------------------------- #
@login_required
def contact_detail(request, contact_id):
    contact = Contact_Us.objects.get(pk=contact_id)
    return render(request, 'main/contact_detail.html', {
        'contact': contact
    })


