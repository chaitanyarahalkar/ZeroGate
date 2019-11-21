from django.db import models


ROLES = [
		("PE", "Production Engineer"),
		("SE", "Security Engineer"),
		("MG", "Manager"),
		("SA", "System Administrator")
]
# Create your models here.
class User(models.Model):
	username = models.CharField(max_length = 30, primary_key = True)
	role = models.CharField(max_length = 2,choices = ROLES, default = "SE")

	def __str__(self):
		return self.username


class Resources(models.Model):
	role = models.CharField(max_length = 2,choices = ROLES, default = "SE")
	score = models.FloatField(default = 0.0)
	service = models.CharField(max_length = 20)

	def __str__(self):
		return self.service
