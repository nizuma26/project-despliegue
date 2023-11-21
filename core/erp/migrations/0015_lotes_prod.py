# Generated by Django 4.1.5 on 2023-06-30 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0014_seriales_disp'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotes',
            name='prod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_lote_set', to='erp.producto'),
        ),
    ]