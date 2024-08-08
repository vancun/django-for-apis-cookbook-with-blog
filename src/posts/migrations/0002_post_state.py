# Generated by Django 5.1 on 2024-08-08 14:33

import django_fsm
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="state",
            field=django_fsm.FSMField(
                choices=[("new", "New")], default="new", max_length=50
            ),
        ),
    ]
