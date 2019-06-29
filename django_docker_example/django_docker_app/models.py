from django.db import models
from .utils import blank_null, maxlength_blank_null


class DDUser(models.Model):
    email = models.CharField(**maxlength_blank_null)
    text = models.TextField(**blank_null)


class Teste1(models.Model):
    email = models.CharField(**maxlength_blank_null)


class Teste2(models.Model):
    email = models.CharField(**maxlength_blank_null)
