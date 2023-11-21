# Generated by Django 4.1.5 on 2023-09-29 19:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=255, null=True)),
                ('mensaje', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('leida', models.BooleanField(default=False)),
                ('usuario', models.ManyToManyField(related_name='notification_user_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('fecha',),
                'permissions': (('view_notificacion', 'Can view notificaciones'),),
                'default_permissions': (),
            },
        ),
    ]
