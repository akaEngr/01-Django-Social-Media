from django.contrib import admin
from .models import UserModel, UserModel_manually
from django.contrib.auth.models import User #* imp
from django.contrib.auth.admin import UserAdmin #* imp
# Register your models here.
admin.site.register(UserModel)
admin.site.register(UserModel_manually)



admin.site.unregister(User) #* imp
@admin.register(User) #* imp
class customUserAdmin(UserAdmin): #* imp
    list_display = ("id", "username", "email", "is_staff", "is_active") #* imp

    