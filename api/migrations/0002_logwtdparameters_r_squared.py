# Generated by Django 3.0.5 on 2021-09-25 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logwtdparameters',
            name='r_squared',
            field=models.FloatField(default=0),
        ),
    ]