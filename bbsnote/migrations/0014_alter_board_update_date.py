# Generated by Django 4.1.7 on 2023-03-30 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbsnote', '0013_alter_board_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]