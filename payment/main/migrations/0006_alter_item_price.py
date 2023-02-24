# Generated by Django 4.1.7 on 2023-02-20 13:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Цена'),
        ),
    ]