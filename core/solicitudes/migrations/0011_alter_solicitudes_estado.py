# Generated by Django 4.1.5 on 2023-10-08 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0010_alter_solicitudes_prioridad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudes',
            name='estado',
            field=models.CharField(choices=[('EN CREACIÓN', 'En creación'), ('EN ESPERA', 'En espera')], default='EN CREACIÓN', max_length=25),
        ),
    ]
