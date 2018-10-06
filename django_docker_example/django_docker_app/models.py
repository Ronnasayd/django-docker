from django.db import models

class DDUser(models.Model):
	email = models.CharField(max_length=255)