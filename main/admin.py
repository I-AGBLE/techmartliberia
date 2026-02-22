from django.contrib import admin

from main.models import About_Us_Hero, Hero_Section, Service, Team_Member, why_us

# Register your models here.
admin.site.register(Hero_Section)
admin.site.register(Service)
admin.site.register(Team_Member)
admin.site.register(why_us)
admin.site.register(About_Us_Hero)