from django.http import HttpResponse
from django.shortcuts import render

from main.models import Hero_Section



# Create your views here.
def index(request):
    return render(request, 'main/index.html', {
        'hero_section': Hero_Section.objects.all()
    })

def contact(request):
    return render(request, 'main/contact.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')

def events(request):
    return render(request, 'main/events.html')

def meet_our_team(request):
    return render(request, 'main/meet_our_team.html')
