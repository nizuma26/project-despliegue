# Generated by Django 4.1.5 on 2023-10-09 00:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0036_remove_concepmovimiento_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codbienes',
            name='created',
        ),
        migrations.RemoveField(
            model_name='codbienes',
            name='updated',
        ),
    ]