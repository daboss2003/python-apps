# Generated by Django 4.2.8 on 2023-12-16 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_notification_post_notification_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True),
        ),
    ]
