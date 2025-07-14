# Aplicaciones/usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login_ciudadano/', views.login_ciudadano, name='login_ciudadano'),
    path('login_funcionario/', views.login_funcionario, name='login_funcionario'),
    path('register_ciudadano/', views.register_ciudadano, name='register_ciudadano'),
    path('register_funcionario/', views.register_funcionario, name='register_funcionario'),
    path('contactos/', views.contactos, name='contactos'), 
    path('usuarios_lista/', views.usuarios_lista),
    path('editar_ciudadano/<int:id>/', views.editar_ciudadano, name='editar_ciudadano'),
    path('procesar_edicion_ciudadano/<int:id>/', views.procesar_edicion_ciudadano, name='procesar_edicion_ciudadano'),
    path('mi_perfil/editar/', views.editar_mi_perfil, name='editar_mi_perfil'),
    path('mi_perfil_funcionario/editar/', views.editar_mi_perfil_funcionario, name='editar_mi_perfil_funcionario'),
    path('funcionarios_lista/', views.funcionarios_lista, name='funcionarios_lista'),
    path('eliminar_funcionario/<id>',views.eliminar_funcionario),
    path('eliminar_ciudadano/<id>',views.eliminar_ciudadano),
]