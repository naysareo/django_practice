# Generated by Django 5.2.1 on 2025-05-22 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('text', models.CharField()),
            ],
            options={
                'verbose_name': 'Main model',
                'verbose_name_plural': 'Main model',
            },
        ),
    ]
