# Generated by Django 4.1.5 on 2023-09-10 22:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erp', '0032_remove_inventariobienes_ant_tipo_proc_and_more'),
        ('solicitudes', '0003_remove_solicsoporte_updated_solicsoporte_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detsolicitud',
            name='inventario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.inventariobienes'),
        ),
        migrations.AlterField(
            model_name='detsolicitud',
            name='productos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitud_productos_set', to='erp.producto'),
        ),
        migrations.AlterField(
            model_name='detsolicitud',
            name='solicitud',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitud_set', to='solicitudes.solicitudes'),
        ),
        migrations.AlterField(
            model_name='solicitudes',
            name='codigo',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitudes',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solicitudes',
            name='estado',
            field=models.CharField(blank=True, choices=[('ECR', 'En Creación'), ('PEN', 'Pendiente'), ('REC', 'Rechazada'), ('RES', 'Resuelta')], default='ECR', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='solicitudes',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='solicitudes',
            name='prioridad',
            field=models.CharField(blank=True, choices=[('MB', 'Muy baja'), ('BJ', 'Baja'), ('NM', 'Normal'), ('AT', 'Alta'), ('MA', 'Muy alta')], default='NM', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='solicitudes',
            name='tipo_solicitud',
            field=models.CharField(choices=[('SDT', 'Solicitud de Distribución'), ('STL', 'Solicitud de Traslado'), ('SDC', 'Solicitud de Desincorporación')], max_length=25),
        ),
        migrations.AlterField(
            model_name='solicitudes',
            name='unidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitud_unidad_set', to='erp.unidad'),
        ),
        migrations.AlterField(
            model_name='solicitudes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitud_user_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
