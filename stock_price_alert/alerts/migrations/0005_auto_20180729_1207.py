# Generated by Django 2.0.7 on 2018-07-29 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0004_auto_20180729_1147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='script_symbol',
            new_name='scrip_symbol',
        ),
    ]
