from django.http import HttpResponse
from django.shortcuts import render

from main.models import Hero_Section, Service, Team_Member



# Create your views here.
def index(request):
    return render(request, 'main/index.html', {
        'hero_section': Hero_Section.objects.all(),
        'team_members': Team_Member.objects.all()
    })

def contact(request):
    return render(request, 'main/contact.html')

def about(request):
    return render(request, 'main/about.html')

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

def events(request):
    return render(request, 'main/events.html')

def meet_our_team(request):
    return render(request, 'main/meet_our_team.html')
