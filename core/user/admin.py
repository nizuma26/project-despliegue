from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.
from core.user.models import User

admin.site.register(User)
admin.site.register(Permission)