# Generated by Django 2.0.2 on 2018-03-30 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission', '0017_auto_20180330_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input',
            name='items',
        ),
        migrations.AddField(
            model_name='input',
            name='item0',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='input',
            name='item1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='input',
            name='item2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='input',
            name='item3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='input',
            name='item4',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='input',
            name='item5',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='input',
            name='item6',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
