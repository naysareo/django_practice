# Generated by Django 5.2.1 on 2025-05-26 14:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_book_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 26, 14, 36, 1, 544336, tzinfo=datetime.timezone.utc)),
        ),
    ]
