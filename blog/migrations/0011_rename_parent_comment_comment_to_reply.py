# Generated by Django 4.1.2 on 2022-11-10 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_comment_options_remove_comment_level_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parent',
            new_name='comment_to_reply',
        ),
    ]