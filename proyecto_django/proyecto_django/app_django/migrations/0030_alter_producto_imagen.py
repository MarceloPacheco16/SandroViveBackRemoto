# Generated by Django 5.0.4 on 2024-11-24 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_django', '0029_alter_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.URLField(blank=True, null=True),
        ),
    ]
