# Generated by Django 4.1.5 on 2023-10-06 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aprobaciones', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aprobaciones',
            old_name='razon',
            new_name='motivo',
        ),
        migrations.AlterField(
            model_name='aprobaciones',
            name='accion',
            field=models.CharField(choices=[('RETORNADA', 'Retornar'), ('APROBADA', 'Aprobar'), ('RECHAZADA', 'Rechazar')], default='APROBADA', max_length=25),
        ),
    ]
