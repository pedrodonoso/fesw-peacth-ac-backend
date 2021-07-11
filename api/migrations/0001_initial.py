# Generated by Django 3.0.5 on 2021-07-10 21:49

import api.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=5, unique=True)),
                ('sex', models.CharField(max_length=1)),
                ('bloodType', models.CharField(max_length=256)),
                ('initialDate', models.CharField(max_length=256)),
                ('initialDosis', models.IntegerField(default=0)),
                ('initialINR', models.FloatField()),
                ('weeklyDosisInRange', models.IntegerField(default=0)),
                ('totalDays', models.IntegerField(default=0)),
                ('weight', models.IntegerField()),
                ('height', models.FloatField()),
                ('imc', models.FloatField()),
                ('age', models.IntegerField(default=0)),
                ('genetics', djongo.models.fields.EmbeddedField(model_container=api.models.Genetic)),
                ('diagnosis', djongo.models.fields.EmbeddedField(model_container=api.models.Diagnosis)),
            ],
        ),
    ]