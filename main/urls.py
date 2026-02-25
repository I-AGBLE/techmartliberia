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
    path('edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('edit_about_us_hero/<int:about_hero_id>/', views.edit_about_us_hero, name='edit_about_us_hero'),
    path('edit_admin_team_member/<int:member_id>/', views.edit_admin_team_member, name='edit_admin_team_member'),
    path('edit_admin_why_us/<int:why_us_id>/', views.edit_admin_why_us, name='edit_admin_why_us'),
    path('add_new_service/', views.add_new_service, name='add_new_service'),
    path('add_new_team_member/', views.add_new_team_member, name='add_new_team_member'),
    path('add_new_why_us/', views.add_new_why_us, name='add_new_why_us'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('delete_team_member/<int:member_id>/', views.delete_team_member, name='delete_team_member'),
    path('delete_why_us/<int:why_us_id>/', views.delete_why_us, name='delete_why_us'),
    path('logout/', views.logout, name='logout'),
    path('contact_us/', views.contact_us, name='contact_us'),
]