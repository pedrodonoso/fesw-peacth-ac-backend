from datetime import datetime
from djongo import models
import datetime

isMigrate = True

# Create your models here.
class Genetic(models.Model):
    CYP2C9_2 = models.CharField(unique=True, max_length=5)
    CYP2C9_3 = models.CharField(unique=True, max_length=5)
    VKORC1 = models.CharField(unique=True, max_length=5)

    class Meta:
        abstract = isMigrate


class Diagnosis(models.Model):
    diagnosis1 = models.CharField(max_length=256)
    diagnosis2 = models.CharField(max_length=256)
    diagnosis3 = models.CharField(max_length=256)
    diagnosis4 = models.CharField(max_length=256)

    class Meta:
        abstract = isMigrate

class Patient(models.Model):
    _id = models.ObjectIdField()
    code = models.CharField(unique=True, max_length=5)
    sex = models.CharField(max_length=1)
    bloodType = models.CharField(max_length=256)
    initialDate = models.DateField(default=datetime.date.today)
    initialDosis = models.FloatField(default=0)
    initialINR = models.FloatField()
    weeklyDosisInRange = models.FloatField(default=0)
    totalDays = models.IntegerField(default=0)
    weight = models.FloatField()
    height = models.FloatField()
    imc = models.FloatField()
    age = models.IntegerField(default=0)

    genetics = models.EmbeddedField(
        model_container=Genetic
    )

    diagnosis = models.EmbeddedField(
        model_container=Diagnosis
    )

    objects = models.DjongoManager()

class ClinicalControl(models.Model):
    _id = models.ObjectIdField()
    patientCode = models.CharField(max_length=5)
    controlDate = models.DateField(default=datetime.date.today)
    arrivalDose = models.FloatField(default=0)
    updatedDose = models.FloatField(default=0)
    arrivalINR = models.FloatField(default=0)
    inrInRange = models.BooleanField(default=False)

class LogWTDparameters(models.Model):
    _id = models.ObjectIdField()
    p_1  = models.FloatField(default=0)
    p_2  = models.FloatField(default=0)
    p_3  = models.FloatField(default=0)
    p_4  = models.FloatField(default=0)
    p_5  = models.FloatField(default=0)
    p_6  = models.FloatField(default=0)
    p_7  = models.FloatField(default=0)
    p_8  = models.FloatField(default=0)
    p_9  = models.FloatField(default=0)
    p_10 = models.FloatField(default=0)