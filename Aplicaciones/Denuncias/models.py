from django.db import models
from Aplicaciones.Usuarios.models import Ciudadano, Funcionario
from cloudinary.models import CloudinaryField
# Create your models here.

class Denuncia(models.Model):
    id = models.AutoField(primary_key=True)
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    referencia = models.CharField(max_length=255)
    estado = models.CharField(max_length=50, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = CloudinaryField('imagen', blank=True, null=True)

    def __str__(self):
        return f"Denuncia de {self.ciudadano.nombre} - {self.tipo}"

class Respuesta(models.Model):
    id = models.AutoField(primary_key=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respuesta de {self.funcionario.nombre} a {self.denuncia.ciudadano.nombre}"