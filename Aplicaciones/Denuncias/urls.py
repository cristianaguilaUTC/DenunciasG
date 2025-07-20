# denuncias/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear_denuncia/', views.crear_denuncia, name='crear_denuncia'),
    path('panel_funcionario/', views.panel_funcionario, name='panel_funcionario'),
    path('eliminar_denuncia/<id>/', views.eliminar_denuncia),
    path('menu/', views.menu, name='menu'),
    path('editar_denuncia/<int:id>/', views.editar_denuncia, name='editar_denuncia'),
    path('denuncias_ciudadanas/', views.denuncias_list, name='denuncias_ciudadanas'),
    path('mis_denuncias/', views.mis_denuncias, name='mis_denuncias'),
    path('responder_denuncia/<int:denuncia_id>/', views.responder_denuncia, name='responder_denuncia'),
    path('reporte_denuncias_completo/', views.reporte_completo_denuncias, name='reporte_completo_denuncias'),
    path('respuesta_lista/', views.respuesta_lista, name='respuesta_lista'),


]