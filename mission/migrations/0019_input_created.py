# Generated by Django 2.0.2 on 2018-04-22 00:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mission', '0018_auto_20180330_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
