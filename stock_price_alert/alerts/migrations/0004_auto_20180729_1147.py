# Generated by Django 2.0.7 on 2018-07-29 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0003_alert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='exchange_name',
            field=models.CharField(max_length=10),
        ),
    ]
