# Generated by Django 5.0.4 on 2024-09-10 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_django', '0015_alter_pedido_fecha_entregada_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido_producto',
            name='total',
        ),
    ]
