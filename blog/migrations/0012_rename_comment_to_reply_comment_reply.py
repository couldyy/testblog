# Generated by Django 4.1.2 on 2022-11-13 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_rename_parent_comment_comment_to_reply'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_to_reply',
            new_name='reply',
        ),
    ]
