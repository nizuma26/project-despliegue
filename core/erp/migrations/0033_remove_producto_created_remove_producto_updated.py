# Generated by Django 4.1.5 on 2023-10-08 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0032_remove_inventariobienes_ant_tipo_proc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='created',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='updated',
        ),
    ]
