from django.urls import path
from .views import registrar_usuario, iniciar_sesion, listar_turnos, reservar_turno, cancelar_turno

urlpatterns = [
    path('api/registro/', registrar_usuario, name='registro'),
    path('api/login/', iniciar_sesion, name='login'),
    path('api/turnos/', listar_turnos, name='listar_turnos'),  # 🚀 Nueva ruta para listar turnos disponibles
    path('api/reservar/', reservar_turno, name='reservar_turno'),  # 🚀 Nueva ruta para reservar turnos
    path('api/cancelar/<int:turno_id>/', cancelar_turno, name='cancelar_turno'),  # 🚀 Nueva ruta para cancelar turnos
]

