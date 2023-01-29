from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Doctor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	identity_card_url = models.CharField(max_length=300, blank=True)
	medical_license_url = models.CharField(max_length=300, blank=True)
	status = models.IntegerField(default=0)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username

class PatientProfile(models.Model):
	patient = models.ForeignKey(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length=300, blank=True)
	birthday = models.CharField(max_length=300, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

class PatientTest(models.Model):
	patient = models.ForeignKey(User, on_delete=models.CASCADE)
	xray_url = models.CharField(max_length=300, blank=True)
	xray_hash = models.CharField(max_length=300, blank=True)
	percentage = models.IntegerField(default=0)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.patient.username

# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()
