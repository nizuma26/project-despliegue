# Generated by Django 4.1.5 on 2023-10-08 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0039_alter_proveedor_ced_repre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codbienes',
            name='procedencia',
        ),
        migrations.RemoveField(
            model_name='codbienes',
            name='unidad_admin',
        ),
        migrations.AlterField(
            model_name='codbienes',
            name='codbien',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='codbienes',
            name='estado',
            field=models.CharField(blank=True, choices=[('ASI', 'Asignado'), ('SAS', 'Sin asignar'), ('ANU', 'Anulado')], default='SAS', max_length=12, null=True),
        ),
    ]