from django.db import models

# Create your models here.

class Usuario(models.Model):
	nome = models.CharField(max_length=255)
	foto = models.ImageField(upload_to='fotos')