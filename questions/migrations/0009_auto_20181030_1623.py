# Generated by Django 2.1.2 on 2018-10-30 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20181030_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentvote',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Comment'),
        ),
    ]
