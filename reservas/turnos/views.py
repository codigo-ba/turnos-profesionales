from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Turno, Usuario
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .utils import enviar_notificacion



# 🚀 Registro de usuario
@api_view(['POST'])
def registrar_usuario(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    is_profesional = request.data.get('is_profesional', False)

    if not username or not email or not password:
        return Response({"error": "Todos los campos son obligatorios."}, status=400)

    if Usuario.objects.filter(username=username).exists():
        return Response({"error": "El nombre de usuario ya está registrado."}, status=400)

    usuario = Usuario.objects.create_user(username=username, email=email, password=password, is_profesional=is_profesional)
    return Response({"mensaje": "Usuario registrado correctamente."}, status=201)

# 🚀 Login con JWT
@api_view(['POST'])
def iniciar_sesion(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=200)
    
    return Response({"error": "Credenciales incorrectas."}, status=401)

@api_view(['GET'])
def listar_turnos(request):
    hoy = datetime.now().date()
    ahora = datetime.now().time()

    # 🚀 Filtrar turnos disponibles (sin reservar y en fechas válidas)
    turnos = Turno.objects.filter(
        reservado=False,
        fecha__gte=hoy  # ✅ Excluir fechas anteriores al día actual
    ).exclude(
        fecha=hoy, hora__lte=ahora  # ✅ Excluir horarios pasados dentro del día actual
    ).values("id", "fecha", "hora", "profesional__username")

    return Response({"turnos_disponibles": list(turnos)}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reservar_turno(request):
    usuario = request.user
    turno_id = request.data.get("turno_id")

    try:
        turno = Turno.objects.get(id=turno_id, reservado=False)
        turno.usuario = usuario
        turno.reservado = True
        turno.save()

        # 🚀 Enviar notificación al usuario
        enviar_notificacion(
            usuario.email,
            "Confirmación de Reserva",
            f"Has reservado un turno el {turno.fecha} a las {turno.hora}."
        )

        # 🚀 Enviar notificación al profesional
        enviar_notificacion(
            turno.profesional.email,
            "Nuevo Turno Reservado",
            f"{usuario.username} ha reservado un turno el {turno.fecha} a las {turno.hora}."
        )

        return Response({"mensaje": "Turno reservado con éxito"}, status=200)

    except Turno.DoesNotExist:
        return Response({"error": "El turno no está disponible"}, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancelar_turno(request, turno_id):
    usuario = request.user

    try:
        turno = Turno.objects.get(id=turno_id, usuario=usuario)
        turno.reservado = False
        turno.usuario = None
        turno.save()

        # 🚀 Enviar notificación al usuario
        enviar_notificacion(
            usuario.email,
            "Cancelación de Turno",
            f"Has cancelado tu turno el {turno.fecha} a las {turno.hora}."
        )

        # 🚀 Enviar notificación al profesional
        enviar_notificacion(
            turno.profesional.email,
            "Turno Cancelado",
            f"{usuario.username} ha cancelado su turno el {turno.fecha} a las {turno.hora}."
        )

        return Response({"mensaje": "Turno cancelado con éxito"}, status=200)

    except Turno.DoesNotExist:
        return Response({"error": "Turno no encontrado o no puedes cancelarlo"}, status=400)

