# Generated by Django 3.1.6 on 2021-02-27 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0002_auto_20210227_1605"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinfo",
            name="price_policy",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="web.pricepolicy",
                verbose_name="价格策略",
            ),
        ),
    ]
