from django.contrib import admin
from .models import User,Advisor

# Register your models here.
#admin.site.register(Advisor)
#admin.site.register(User)

@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ['name','photo']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','email']
