# Generated by Django 5.0 on 2023-12-21 09:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_library', '0005_alter_book_book_add_datetime_alter_lend_lend_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='num',
        ),
        migrations.AlterField(
            model_name='book',
            name='book_add_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 21, 9, 17, 15, 378295, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='lend',
            name='lend_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 21, 9, 17, 15, 380805, tzinfo=datetime.timezone.utc)),
        ),
    ]
