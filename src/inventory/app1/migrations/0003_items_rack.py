# Generated by Django 3.0.3 on 2020-02-24 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_items_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='rack',
            field=models.CharField(default='', max_length=500),
        ),
    ]