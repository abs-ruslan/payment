# Generated by Django 4.1.7 on 2023-02-20 12:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_item_options_alter_item_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Цена'),
        ),
    ]
