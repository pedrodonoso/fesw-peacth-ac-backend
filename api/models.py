from djongo import models

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
    initialDate = models.CharField(max_length=256)
    initialDosis = models.FloatField(default=0)
    initialINR = models.FloatField()
    weeklyDosisInRange = models.IntegerField(default=0)
    totalDays = models.IntegerField(default=0)
    weight = models.IntegerField()
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