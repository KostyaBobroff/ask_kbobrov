# Generated by Django 2.1.2 on 2018-11-01 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20181101_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='rating',
        ),
    ]
