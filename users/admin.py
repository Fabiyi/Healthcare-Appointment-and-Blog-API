from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group
# Register your models here.



class CustomUserAdmin(admin.ModelAdmin):
    list_display =('last_name','email','is_staff','is_active','role','id')
    search_fields = ('first_name','email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)