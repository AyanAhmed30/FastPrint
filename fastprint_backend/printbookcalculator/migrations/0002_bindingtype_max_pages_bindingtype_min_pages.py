# Generated by Django 4.2.21 on 2025-06-27 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printbookcalculator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bindingtype',
            name='max_pages',
            field=models.IntegerField(default=10000),
        ),
        migrations.AddField(
            model_name='bindingtype',
            name='min_pages',
            field=models.IntegerField(default=0),
        ),
    ]
