# Generated by Django 4.1.5 on 2023-11-02 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0043_alter_categoria_options_alter_desincalmacen_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlstock',
            name='almacenes',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_almacen_set', to='erp.almacen'),
        ),
        migrations.AlterField(
            model_name='controlstock',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='controlstock',
            name='productos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.producto'),
        ),
        migrations.AlterField(
            model_name='controlstock',
            name='stock_actual',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='controlstock',
            name='stock_max',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='controlstock',
            name='stock_min',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
