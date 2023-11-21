# Generated by Django 4.1.5 on 2023-09-13 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0007_remove_solicitudes_departamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudes',
            name='tipo_solicitud',
            field=models.CharField(choices=[('DIST', 'Solicitud de Distribución'), ('TRAS', 'Solicitud de Traslado'), ('DES_USO', 'Solicitud de Desincorporación de Bienes Muebles en uso'), ('DES_DEPOSITO', 'Solicitud de Desincorporación de Bienes en Depósito')], max_length=25),
        ),
    ]