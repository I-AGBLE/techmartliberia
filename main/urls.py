from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'), 
    path('service_page/<int:service_id>/', views.service_page, name='service_page'),
    path('user_in/', views.user_in, name='user_in'),
    path('user_dash/', views.user_dash, name='user_dash'),
    path('edit_hero/<int:hero_id>/', views.edit_hero, name='edit_hero'),
]