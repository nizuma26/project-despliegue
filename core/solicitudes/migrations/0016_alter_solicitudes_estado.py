# Generated by Django 4.1.5 on 2023-11-08 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0015_alter_detsolicitud_aprobado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudes',
            name='estado',
            field=models.CharField(choices=[('EN CREACIÓN', 'En creación'), ('EN ESPERA', 'En espera')], default='EN ESPERA', max_length=25),
        ),
    ]