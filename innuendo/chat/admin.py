from django.contrib import admin

# Register your models here.
from .models import Group, Message, User

admin.site.register(Group)
admin.site.register(Message)
admin.site.register(User)