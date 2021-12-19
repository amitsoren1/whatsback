from django.contrib import admin

# Register your models here.
from .models import User, Profile, Contact
from django.contrib.auth.models import Group

admin.site.unregister(Group)
# admin.site.register(User)

@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    fields = ["phone", "password", "is_superuser"]

admin.site.register(Profile)
admin.site.register(Contact)
