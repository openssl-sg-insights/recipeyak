# Generated by Django 2.0.2 on 2018-06-30 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_auto_20180624_1825'),
    ]

    migrations.RunSQL(
        """
        ALTER TABLE core_scheduledrecipe ADD CONSTRAINT owner_required CHECK (
            (team_id IS NOT NULL) OR (user_id IS NOT NULL)
        );
        """,
        """
        ALTER TABLE core_scheduledrecipe DROP CONSTRAINT owner_selected;
        """
    )