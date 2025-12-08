from django.db import models
from medication.models import Patient
# Create your models here.

class healthProfile(models.Model):
    patient=models.OneToOneField(Patient,on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    disease =  models.TextField()
    addition_info = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.patient.name} - Profile"
    
class HealthPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    food_chart = models.TextField()
    exercise_plan = models.TextField()
    sleep_plan = models.TextField(null=True,blank=True)
    generated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plan for {self.patient.name}"   
class DailyProgress(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date= models.DateField(auto_now=True)
    water_intake_liter = models.FloatField(default=0)
    steps_walked = models.IntegerField(default=0)
    calories_consumed = models.IntegerField(default=0)
    mood = models.CharField(max_length=50,null=True,blank=True)
    progress_note =models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Progress {self.patient.name} - {self.date}"  

