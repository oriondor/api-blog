# Generated by Django 3.1.2 on 2020-10-24 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogger_app_main', '0003_blog_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='read',
            name='blog',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='blogger_app_main.blog'),
            preserve_default=False,
        ),
    ]
