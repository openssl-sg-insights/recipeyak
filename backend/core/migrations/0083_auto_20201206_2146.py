# Generated by Django 2.2.12 on 2020-12-06 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0082_recipe_archived_at")]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="scheduledrecipe",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="section",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="step",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="team",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
