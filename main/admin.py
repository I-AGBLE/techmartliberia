from django.contrib import admin

from main.models import Hero_Section, Service, Team_Member, why_us

# Register your models here.
admin.site.register(Hero_Section)
admin.site.register(Service)
admin.site.register(Team_Member)
admin.site.register(why_us)