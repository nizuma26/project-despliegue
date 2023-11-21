# Generated by Django 4.1.5 on 2023-10-02 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notificaciones', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificacion',
            name='usuario',
        ),
        migrations.AddField(
            model_name='notificacion',
            name='usuario_emisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_user_origen_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='usuario_receptor',
            field=models.ManyToManyField(related_name='notification_user_destino_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
