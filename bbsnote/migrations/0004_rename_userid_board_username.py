# Generated by Django 4.1.7 on 2023-03-27 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbsnote', '0003_board_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='userID',
            new_name='username',
        ),
    ]
