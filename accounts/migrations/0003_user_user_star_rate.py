# Generated by Django 2.1 on 2019-08-06 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190731_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_star_rate',
            field=models.IntegerField(default=0),
        ),
    ]
