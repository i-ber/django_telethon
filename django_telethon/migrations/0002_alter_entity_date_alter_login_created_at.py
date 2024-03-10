# Generated by Django 5.0.2 on 2024-03-07 13:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_telethon", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entity",
            name="date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Date"
            ),
        ),
        migrations.AlterField(
            model_name="login",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Created at"
            ),
        ),
    ]