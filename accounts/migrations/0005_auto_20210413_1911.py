# Generated by Django 3.1.7 on 2021-04-13 19:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_auto_20210413_1851'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='phoneOTP',
            new_name='PhoneDb',
        ),
    ]
