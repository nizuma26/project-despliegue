# Generated by Django 4.1.5 on 2023-10-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui_customizer', '0004_alter_customizer_sidebar_orientation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customizer',
            name='sidebar_orientation',
            field=models.CharField(blank=True, default='vtc', max_length=25, null=True),
        ),
    ]
