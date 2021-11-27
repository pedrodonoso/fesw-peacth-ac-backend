# Generated by Django 3.0.5 on 2021-11-27 23:20

import api.models
import datetime
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClinicalControl',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('patientCode', models.CharField(max_length=5)),
                ('controlDate', models.DateField(default=datetime.date.today)),
                ('arrivalDose', models.FloatField(default=0)),
                ('updatedDose', models.FloatField(default=0)),
                ('arrivalINR', models.FloatField(default=0)),
                ('inrInRange', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LogWTDparameters',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('p_0', models.FloatField(default=0)),
                ('p_men', models.FloatField(default=0)),
                ('p_age', models.FloatField(default=0)),
                ('p_initialINR', models.FloatField(default=0)),
                ('p_imc', models.FloatField(default=0)),
                ('p_CYP2C9_12', models.FloatField(default=0)),
                ('p_CYP2C9_13', models.FloatField(default=0)),
                ('p_CYP2C9_33', models.FloatField(default=0)),
                ('p_VKORC1_GA', models.FloatField(default=0)),
                ('p_VKORC1_AA', models.FloatField(default=0)),
                ('r_squared', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ModelsResults',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=5, unique=True)),
                ('network_result', models.FloatField(default=0)),
                ('regression_result', models.FloatField(default=0)),
                ('network_error', models.FloatField(default=0)),
                ('regression_error', models.FloatField(default=0)),
                ('final_dose', models.FloatField(default=0)),
                ('is_treatement_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=5, unique=True)),
                ('sex', models.CharField(max_length=1)),
                ('initialDate', models.DateField(default=datetime.date.today)),
                ('initialDose', models.FloatField(default=0)),
                ('initialINR', models.FloatField()),
                ('weeklyDoseInRange', models.FloatField(default=0)),
                ('totalDays', models.IntegerField(default=0)),
                ('weight', models.FloatField()),
                ('height', models.FloatField()),
                ('imc', models.FloatField()),
                ('age', models.IntegerField(default=0)),
                ('genetics', djongo.models.fields.EmbeddedField(model_container=api.models.Genetic)),
            ],
        ),
    ]
