from django.contrib import admin

# Register your models here.
from .models import Chat, Message


admin.site.register(Chat)
admin.site.register(Message)

# class CustomModelAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Chat._meta.fields]
#     readonly_fields = ('id',)

# admin.site.register(Chat, CustomModelAdmin)
# admin.site.register(Message, CustomModelAdmin)