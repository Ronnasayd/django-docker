from django.db import models
from .utils import blank_null


class DDUser(models.Model):
	email = models.CharField(max_length=255, **blank_null)
