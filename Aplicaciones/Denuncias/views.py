from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Denuncia, Respuesta
from Aplicaciones.Usuarios.models import Ciudadano, Funcionario
from django.conf import settings

#graficas
from django.db.models.functions import TruncDate,TruncMonth
from django.db.models import Count
from .models import Denuncia,Respuesta
import calendar

#calendario
import json

def reporte_completo_denuncias(request):
    # Día
    denuncias_por_dia = (
        Denuncia.objects
        .annotate(fecha=TruncDate('fecha_creacion'))
        .values('fecha')
        .annotate(total=Count('id'))
        .order_by('fecha')
    )
    fechas_dia = [d['fecha'].strftime("%Y-%m-%d") for d in denuncias_por_dia]
    totales_dia = [d['total'] for d in denuncias_por_dia]

    # Mes
    denuncias_por_mes = (
        Denuncia.objects
        .annotate(mes=TruncMonth('fecha_creacion'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    etiquetas_mes = [f"{calendar.month_name[d['mes'].month]} {d['mes'].year}" for d in denuncias_por_mes]
    totales_mes = [d['total'] for d in denuncias_por_mes]

    return render(request, "reporte_denuncias_completo.html", {
        'fechas_dia': fechas_dia,
        'totales_dia': totales_dia,
        'etiquetas_mes': etiquetas_mes,
        'totales_mes': totales_mes,
    })


# Create your views here.

def panel_funcionario(request):
    denuncias = Denuncia.objects.all()
    return render(request, "panel_funcionario.html", {"denuncias": denuncias})



def crear_denuncia(request):
    if request.method == "POST":
        tipo = request.POST["tipo"]
        descripcion = request.POST["descripcion"]
        imagenSubiendo=request.FILES.get("imagen") 
        latitud = request.POST["latitud"]
        longitud = request.POST["longitud"]
        referencia = request.POST["referencia"]
        ciudadano = Ciudadano.objects.get(id=request.session["usuario_id"])
        Denuncia.objects.create(
            ciudadano=ciudadano,
            tipo=tipo,
            descripcion=descripcion,
            imagen=imagenSubiendo,
            latitud=latitud,
            longitud=longitud,
            referencia=referencia
        )
        messages.success(request, "Denuncia creada exitosamente")
        return redirect("mis_denuncias")
    return render(request, "crear_denuncia.html")



def responder_denuncia(request, denuncia_id):
    denuncia = Denuncia.objects.get(id=denuncia_id)
    funcionario = Funcionario.objects.get(id=request.session["usuario_id"])

    if request.method == "POST":
        mensaje = request.POST["mensaje"]
        Respuesta.objects.create(
            funcionario=funcionario,
            denuncia=denuncia,
            mensaje=mensaje
        )
        denuncia.estado = "Revisada"
        denuncia.save()

        # Enviar correo
        send_mail(
            subject="Respuesta a su denuncia",
            message=f"Su denuncia fue revisada:\n\n{mensaje}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[denuncia.ciudadano.correo],
            fail_silently=False,
        )

        messages.success(request, "Respuesta enviada exitosamente")
        return redirect("panel_funcionario")

    return render(request, "responder_denuncia.html", {"denuncia": denuncia})


def menu(request):
    return render(request, "menu.html")




def editar_denuncia(request, id):
    try:
        denuncia = Denuncia.objects.get(id=id)
    except Denuncia.DoesNotExist:
        messages.error(request, "Denuncia no encontrada")
        return redirect('panel_funcionario')

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        descripcion = request.POST.get("descripcion")
        estado = request.POST.get("estado")

        # Actualizar los campos de la denuncia
        denuncia.tipo = tipo
        denuncia.descripcion = descripcion
        denuncia.estado = estado
        denuncia.save()

        messages.success(request, "Denuncia actualizada exitosamente")
        return redirect('panel_funcionario')

    return render(request, "editar_denuncia.html", {"denuncia": denuncia})



def denuncias_list(request):
    denuncias = Denuncia.objects.all()
    return render(request, 'denuncias_ciudadanas.html', {'denuncias': denuncias})


def mis_denuncias(request):
    # Verifica si el usuario está logueado como ciudadano
    if "usuario_id" not in request.session or request.session.get("tipo_usuario") != "ciudadano":
        messages.error(request, "Debes iniciar sesión como ciudadano.")
        return redirect("login_ciudadano")  # Ajusta si el nombre de la URL es otro

    ciudadano_id = request.session["usuario_id"]
    denuncias = Denuncia.objects.filter(ciudadano_id=ciudadano_id).order_by("-fecha_creacion")

    return render(request, "mis_denuncias.html", {"denuncias": denuncias})


def eliminar_denuncia(request,id):
    Eliminar=Denuncia.objects.get(id=id)
    Eliminar.delete()
    messages.success(request,"Eliminado exitosamente")
    return redirect('panel_funcionario')




def respuesta_lista(request):
    respuestas = Respuesta.objects.select_related(
        'denuncia__ciudadano', 'funcionario'
    ).all().order_by('-fecha_respuesta')
    return render(request, 'respuesta_lista.html', {'respuestas': respuestas})



def calendario(request):
    denuncias = Denuncia.objects.all()
    temas_list = []

    for denuncia in denuncias:
        # Verificamos si existe una respuesta asociada
        tiene_respuesta = Respuesta.objects.filter(denuncia=denuncia).exists()

        # Definimos el color: verde si tiene respuesta, azul si no
        color_evento = '#28a745' if tiene_respuesta else "#ff0000"

        temas_list.append({
            'id': denuncia.id,
            'title': f"{denuncia.tipo}",
            'start': denuncia.fecha_creacion.isoformat(),
            'color': color_evento,
            'url': f"/responder_denuncia/{denuncia.id}/",  # redirección al hacer clic
        })

    return render(request, 'calendario.html', {
        'temas_json': json.dumps(temas_list)
    })