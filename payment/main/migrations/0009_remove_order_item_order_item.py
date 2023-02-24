# Generated by Django 4.1.7 on 2023-02-22 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ManyToManyField(to='main.item', verbose_name='Товар'),
        ),
    ]