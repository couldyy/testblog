# Generated by Django 4.1.2 on 2022-11-22 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_like_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Количество лайков'),
        ),
    ]