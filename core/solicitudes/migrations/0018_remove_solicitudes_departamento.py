# Generated by Django 4.1.5 on 2023-11-11 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0017_remove_solicitudes_unidad_solicitudes_departamento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudes',
            name='departamento',
        ),
    ]
