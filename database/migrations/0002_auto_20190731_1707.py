# Generated by Django 2.1 on 2019-07-31 17:07

from django.conf import settings
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinghistory',
            name='date',
        ),
        migrations.RemoveField(
            model_name='bookinghistory',
            name='movie_id',
        ),
        migrations.RemoveField(
            model_name='bookinghistory',
            name='screen',
        ),
        migrations.RemoveField(
            model_name='bookinghistory',
            name='user',
        ),
        migrations.AddField(
            model_name='movie',
            name='wish_movie',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='schedule_time',
            name='type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(0, '디지털'), (1, '3D'), (2, '4D'), (3, 'ATMOS'), (4, '자막'), (5, '더빙')], max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='BookingHistory',
        ),
    ]
