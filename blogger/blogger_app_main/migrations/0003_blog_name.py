# Generated by Django 3.1.2 on 2020-10-24 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger_app_main', '0002_auto_20201023_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='name',
            field=models.CharField(default='My Blog', max_length=20),
        ),
    ]
