from django.test import TestCase
from Aplicaciones.Usuarios.models import Ciudadano, Funcionario

class CiudadanoFuncionarioCRUDTest(TestCase):
    def setUp(self):
        self.ciudadano = Ciudadano.objects.create(
            cedula="1111111111", nombre="Pedro", apellido="Sanchez",
            telefono="0123456789", correo="pedro@mail.com", contrasena="pass123"
        )
        self.funcionario = Funcionario.objects.create(
            nombre="Lucia", apellido="Martinez", telefono="0123456789",
            correo="lucia@mail.com", contrasena="funcpass"
        )

    def test_crear_ciudadano(self):
        self.assertEqual(Ciudadano.objects.count(), 1)

    def test_editar_ciudadano(self):
        self.ciudadano.nombre = "Carlos"
        self.ciudadano.save()
        self.assertEqual(Ciudadano.objects.get(id=self.ciudadano.id).nombre, "Carlos")

    def test_eliminar_ciudadano(self):
        self.ciudadano.delete()
        self.assertEqual(Ciudadano.objects.count(), 0)

    def test_crear_funcionario(self):
        self.assertEqual(Funcionario.objects.count(), 1)

    def test_editar_funcionario(self):
        self.funcionario.nombre = "Maria"
        self.funcionario.save()
        self.assertEqual(Funcionario.objects.get(id=self.funcionario.id).nombre, "Maria")

    def test_eliminar_funcionario(self):
        self.funcionario.delete()
        self.assertEqual(Funcionario.objects.count(), 0)
