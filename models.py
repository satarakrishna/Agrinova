from django.db import models


class CropAdvice(models.Model):
	crop = models.CharField(max_length=100)
	region = models.CharField(max_length=100, blank=True)
	what_to_do = models.TextField()
	how_to_do = models.TextField()
	when_to_do = models.TextField()

	def __str__(self):
		return f"{self.crop} ({self.region})"
