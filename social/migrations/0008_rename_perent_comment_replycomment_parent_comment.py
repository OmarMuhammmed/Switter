# Generated by Django 5.1 on 2024-09-25 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_alter_replycomment_perent_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='replycomment',
            old_name='perent_comment',
            new_name='parent_comment',
        ),
    ]
