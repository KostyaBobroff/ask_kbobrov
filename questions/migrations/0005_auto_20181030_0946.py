# Generated by Django 2.1.2 on 2018-10-30 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20181029_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='votes',
            field=models.ManyToManyField(blank=True, related_name='questions', to='questions.QuestionVote'),
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='comment',
            field=models.ForeignKey(on_delete=True, to='questions.Comment'),
        ),
        migrations.AlterField(
            model_name='questionvote',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question'),
        ),
    ]