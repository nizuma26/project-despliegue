# Generated by Django 4.1.5 on 2023-11-05 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0013_detsolicitud_cantidad_aprobada'),
    ]

    operations = [
        migrations.AddField(
            model_name='detsolicitud',
            name='aprobado',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
