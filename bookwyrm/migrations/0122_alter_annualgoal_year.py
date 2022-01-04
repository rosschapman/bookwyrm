# Generated by Django 3.2.5 on 2022-01-04 18:59

import bookwyrm.models.user
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookwyrm", "0121_user_summary_keys"),
    ]

    operations = [
        migrations.AlterField(
            model_name="annualgoal",
            name="year",
            field=models.IntegerField(default=bookwyrm.models.user.get_current_year),
        ),
    ]
