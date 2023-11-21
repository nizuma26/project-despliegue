from django.contrib import admin
from django.contrib.auth.models import Group, ContentType

# Re-register GroupAdmin

admin.site.register(ContentType)