# Generated by Django 2.0.2 on 2018-03-13 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mission', '0013_auto_20180313_1152'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='input',
            unique_together={('username', 'region')},
        ),
    ]
