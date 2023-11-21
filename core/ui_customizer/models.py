from django.db import models
from datetime import datetime
# Django
from core.erp.models import *
from core.user.models import User
from django.forms import model_to_dict

# Create your models here.
class Customizer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customizer_user_set')    
    nav_link = models.CharField(max_length=25, default='theme_blue')
    sidebar_theme = models.CharField(max_length=25, default='sidebar-dark-primary', null=False, blank=False)
    brand_logo_theme = models.CharField(max_length=25, blank=True, null=True)
    navbar_theme = models.CharField(max_length=25, default='theme_blue')
    navbar_fixed = models.CharField(max_length=25, blank=True, null=True)
    main_theme = models.CharField(max_length=25, blank=True, null=True)
    sidebar_collapse = models.CharField(max_length=25, blank=True, null=True)
    sidebar_fixed = models.CharField(max_length=25, blank=True, null=True)
    sidebar_flat = models.CharField(max_length=25, blank=True, null=True)
    sidebar_orientation = models.CharField(max_length=25, default='vtc', blank=True, null=True)
    sidebar_legacy = models.CharField(max_length=25, blank=True, null=True)
    sidebar_disable_hover = models.CharField(max_length=25, blank=True, null=True)
    small_body = models.CharField(max_length=25, blank=True, null=True)
    small_navbar = models.CharField(max_length=25, blank=True, null=True)
    small_brand = models.CharField(max_length=25, blank=True, null=True)
    small_sidebar_nav = models.CharField(max_length=25, blank=True, null=True)
    small_footer = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Personalización de Interfaz'
        verbose_name_plural = 'Personalizaciones de Interfaz'
        default_permissions = ()
        permissions = (
            ('advanced_customizations', 'Can change advanced interface'),
            ('basic_customizations', 'Can change basic interface'),
        )
        ordering = ['id']