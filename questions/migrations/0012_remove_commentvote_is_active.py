# Generated by Django 2.1.2 on 2018-11-01 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0011_remove_comment_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentvote',
            name='is_active',
        ),
    ]
