# Generated by Django 4.2.1 on 2023-08-05 10:09

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.profile_avatar_directory_path, verbose_name=''),
        ),
    ]
