from djongo import models

# Create your models here.
class Patient(models.Model):
    _id = models.ObjectIdField()
    code = models.CharField(unique=True, max_length=5)
    sex = models.CharField(max_length=1)
    bloodType = models.CharField(max_length=256)
    initialDate = models.CharField(max_length=256)
    initialDosis = models.IntegerField()
    initialINR = models.FloatField()
    weeklyDosisInRange = models.IntegerField()
    totalDays = models.IntegerField()
    weight = models.IntegerField()
    height = models.FloatField()
    imc = models.FloatField()
    age = models.IntegerField(default=0)
