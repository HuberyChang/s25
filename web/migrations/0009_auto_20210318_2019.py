# Generated by Django 3.1.6 on 2021-03-18 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0008_filerepository"),
    ]

    operations = [
        migrations.RenameField(
            model_name="filerepository",
            old_name="update_datatime",
            new_name="update_datetime",
        ),
    ]
