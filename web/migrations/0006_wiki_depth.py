# Generated by Django 3.1.6 on 2021-03-03 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20210302_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='wiki',
            name='depth',
            field=models.IntegerField(default=1, verbose_name='深度'),
        ),
    ]