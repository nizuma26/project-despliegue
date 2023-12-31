# Generated by Django 4.1.5 on 2023-09-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0008_alter_solicitudes_tipo_solicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudes',
            name='tipo_solicitud',
            field=models.CharField(choices=[('DIST', 'Solicitud de Distribución'), ('TRAS', 'Solicitud de Traslado'), ('DES_USO', 'Solicitud de Desincorporación de Bienes Muebles en Uso'), ('DES_DEPOSITO', 'Solicitud de Desincorporación de Bienes Muebles en Depósito y Materiales de Consumo')], max_length=25),
        ),
    ]
