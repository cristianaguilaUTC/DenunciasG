from django.db import models

# Create your models here.

class Ciudadano(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Funcionario(models.Model):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    contrasena = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    

    