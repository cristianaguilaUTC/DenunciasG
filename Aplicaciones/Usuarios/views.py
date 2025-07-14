from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ciudadano,Funcionario


def home(request):
    return redirect('menu')


def usuarios_lista(request):
    ciudadanos = Ciudadano.objects.all()
    return render(request, "usuarios_lista.html", {"ciudadanos": ciudadanos})

def contactos(request):
    return render(request, 'contactos.html')

def register_ciudadano(request):
    if request.method == "POST":
        cedula = request.POST["cedula"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        correo = request.POST["correo"]
        contrasena = request.POST["contrasena"]
        
        try:
            nuevo_ciudadano = Ciudadano.objects.create(
                cedula=cedula,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                contrasena=contrasena
            )
            messages.success(request, "Registro exitoso. Puedes iniciar sesión ahora.")
            return redirect('login_ciudadano')
        except Exception as e:
            messages.error(request, "Error al registrar. Por favor, verifica los datos ingresados.")
    return render(request, "register_ciudadano.html")




def register_funcionario(request):
    if request.method == "POST":
        correo = request.POST["correo"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        contrasena = request.POST["contrasena"]
        
        try:
            nuevo_funcionario = Funcionario.objects.create(
                correo=correo,
                nombre=nombre,
                apellido=apellido,
                contrasena=contrasena
            )
            messages.success(request, "Registro exitoso. Puedes iniciar sesión ahora.")
            return redirect('login_funcionario')
        except Exception as e:
            messages.error(request, "Error al registrar. Por favor, verifica los datos ingresados.")
    return render(request, "register_funcionario.html")


def login_ciudadano(request):
    if request.method == "POST":
        cedula = request.POST["cedula"]
        contrasena = request.POST["contrasena"]
        try:
            usuario = Ciudadano.objects.get(cedula=cedula, contrasena=contrasena)
            request.session["usuario_id"] = usuario.id
            request.session["tipo_usuario"] = "ciudadano"
            messages.success(request, "Inicio de sesión exitoso")
            return redirect("mis_denuncias")
        except Ciudadano.DoesNotExist:
            messages.error(request, "Credenciales inválidas")
    return render(request, "login_ciudadano.html")

def login_funcionario(request):
    if request.method == "POST":
        correo = request.POST["correo"]
        contrasena = request.POST["contrasena"]
        try:
            usuario = Funcionario.objects.get(correo=correo, contrasena=contrasena)
            request.session["usuario_id"] = usuario.id
            request.session["tipo_usuario"] = "funcionario"
            # si es admin
            if usuario.correo == "admin@gmail.com":
                request.session["es_admin"] = True
            else:
                request.session["es_admin"] = False
            messages.success(request, "Inicio de sesión exitoso")
            return redirect("panel_funcionario")
        except Funcionario.DoesNotExist:
            messages.error(request, "Credenciales inválidas")
    return render(request, "login_funcionario.html")


   
def editar_c(request, id):
    try:
        ciudadano = Ciudadano.objects.get(id=id)
    except Ciudadano.DoesNotExist:
        messages.error(request, "Ciudadano no encontrado")
        return redirect('mis_denuncias')
    
    return render(request, "editar_c.html", {"ciudadano": ciudadano})

def procesar_edicion_ciudadano(request, id):
    try:
        ciudadano = Ciudadano.objects.get(id=id)
    except Ciudadano.DoesNotExist:
        messages.error(request, "Ciudadano no encontrado")
        return redirect('mis_denuncias')

   # Extraer datos del formulario
    cedula = request.POST.get("cedula")
    nombre = request.POST.get("nombre")
    apellido = request.POST.get("apellido")
    correo = request.POST.get("correo")
    contrasena = request.POST.get("contrasena")

   # Actualizar campos
    ciudadano.cedula = cedula
    ciudadano.nombre = nombre
    ciudadano.apellido = apellido
    ciudadano.correo = correo
    ciudadano.contrasena = contrasena
    ciudadano.save()

    messages.success(request, "Ciudadano actualizado exitosamente")
    return redirect("mis_denuncias")


def editar_mi_perfil(request):
    if "usuario_id" not in request.session:
        messages.error(request, "Debes iniciar sesión primero.")
        return redirect("login_ciudadano")

    ciudadano = Ciudadano.objects.get(id=request.session["usuario_id"])

    if request.method == "POST":
        ciudadano.cedula = request.POST.get("cedula")
        ciudadano.nombre = request.POST.get("nombre")
        ciudadano.apellido = request.POST.get("apellido")
        ciudadano.correo = request.POST.get("correo")
        ciudadano.contrasena = request.POST.get("contrasena")
        ciudadano.save()
        messages.success(request, "Tus datos fueron actualizados correctamente.")
        return redirect("mis_denuncias")

    return render(request, "editar_ciudadano.html", {"ciudadano": ciudadano})


def editar_mi_perfil_funcionario(request):
    if "usuario_id" not in request.session or request.session.get("tipo_usuario") != "funcionario":
        messages.error(request, "Debes iniciar sesión como funcionario.")
        return redirect("login_funcionario")

    funcionario = Funcionario.objects.get(id=request.session["usuario_id"])

    if request.method == "POST":
        funcionario.nombre = request.POST.get("nombre")
        funcionario.apellido = request.POST.get("apellido")
        funcionario.correo = request.POST.get("correo")
        funcionario.contrasena = request.POST.get("contrasena")
        funcionario.save()
        messages.success(request, "Tus datos fueron actualizados correctamente.")
        return redirect("panel_funcionario")

    return render(request, "editar_funcionario.html", {"funcionario": funcionario})


def funcionarios_lista(request):
    funcionarios = Funcionario.objects.all()
    return render(request, "funcionarios_lista.html", {"funcionarios": funcionarios})




def eliminar_funcionario(request,id):
    Eliminar=Funcionario.objects.get(id=id)
    Eliminar.delete()
    messages.success(request,"Eliminado exitosamente")
    return redirect('funcionarios_lista')

def eliminar_ciudadano(request,id):
    Eliminar=Ciudadano.objects.get(id=id)
    Eliminar.delete()
    messages.success(request,"Eliminado exitosamente")
    return redirect('usuarios_lista')