from django.test import TestCase
from Aplicaciones.Denuncias.models import Denuncia, Respuesta
from Aplicaciones.Usuarios.models import Ciudadano, Funcionario

class DenunciaRespuestaCRUDTest(TestCase):
    def setUp(self):
        self.ciudadano = Ciudadano.objects.create(
            cedula="1234567890", nombre="Juan", apellido="Perez",
            telefono="0999999999", correo="juan@mail.com", contrasena="1234"
        )
        self.funcionario = Funcionario.objects.create(
            nombre="Ana", apellido="Lopez", telefono="0888888888",
            correo="ana@mail.com", contrasena="abcd"
        )
        self.denuncia = Denuncia.objects.create(
            ciudadano=self.ciudadano, tipo="Robo", descripcion="Algo pasó",
            latitud=-1.23, longitud=-78.56, referencia="Cerca del parque"
        )
        self.respuesta = Respuesta.objects.create(
            funcionario=self.funcionario, denuncia=self.denuncia,
            mensaje="Estamos investigando"
        )

    def test_crear_denuncia(self):
        self.assertEqual(Denuncia.objects.count(), 1)

    def test_editar_denuncia(self):
        self.denuncia.estado = "Atendida"
        self.denuncia.save()
        self.assertEqual(Denuncia.objects.get(id=self.denuncia.id).estado, "Atendida")

    def test_eliminar_denuncia(self):
        self.denuncia.delete()
        self.assertEqual(Denuncia.objects.count(), 0)

    def test_crear_respuesta(self):
        self.assertEqual(Respuesta.objects.count(), 1)

    def test_editar_respuesta(self):
        self.respuesta.mensaje = "Caso cerrado"
        self.respuesta.save()
        self.assertEqual(Respuesta.objects.get(id=self.respuesta.id).mensaje, "Caso cerrado")

    def test_eliminar_respuesta(self):
        self.respuesta.delete()
        self.assertEqual(Respuesta.objects.count(), 0)
