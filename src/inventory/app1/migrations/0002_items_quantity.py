# Generated by Django 3.0.3 on 2020-02-20 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
