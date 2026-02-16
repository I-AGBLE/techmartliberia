from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'), 
    path('events/', views.events, name='events'),
    path('meet_our_team/', views.meet_our_team, name='meet_our_team'),
]