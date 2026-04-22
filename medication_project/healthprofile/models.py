from django.db import models
from medication.models import Patient
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class healthProfile(models.Model):
    user = models.OneToOneField(User, default=None,on_delete=models.CASCADE)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    age = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(120)
        ]
    )
    weight = models.FloatField(
        validators=[MinValueValidator(1)]
    )
    height_feet = models.FloatField(
        default=5,
        validators=[MinValueValidator(0.3)]
    )
    height_inches = models.FloatField(default=0,
        validators=[MinValueValidator(0)]
    )
    bmi = models.FloatField( null=True, blank=True)
    disease = models.TextField()
    addition_info = models.TextField(null=True, blank=True)

    def clean(self):
        print("clean called...")

        if not self.height_feet or self.weight is None:
            return

        # Convert to total inches first
        total_inches = (self.height_feet * 12) + (self.height_inches or 0)

        # Convert inches → meters
        height_in_m = total_inches * 0.0254

        # Weight assumed in kg
        bmi = self.weight / (height_in_m ** 2)

        # if bmi < 10 or bmi > 60:
        #     raise ValidationError('The calculated BMI is out of realistic range.')

        self.bmi = round(bmi, 2)
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
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

    def clean(self):
        if self.progress_note and len(self.progress_note) <20:
           raise ValidationError({"progress_note: it must be greater then 20 character"})
        if self.mood and len(self.mood) <3:
           raise ValidationError({"mood: it must be greater then 3 character"})
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Progress {self.patient.name} - {self.date}" 
class DietaryRecommendation(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    breakfast = models.TextField()
    lunch = models.TextField()
    dinner = models.TextField()
    snacks = models.TextField(null=True,blank=True)
    food_to_avoid = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return f"Dietary Recommendation for {self.patient.name} on {self.created_at.date()}"     
class ExerciseRecommendation(models.Model):
    Patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    recommendation = models.TextField()

