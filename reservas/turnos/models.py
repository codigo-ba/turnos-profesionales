from django.contrib.auth.models import AbstractUser
from django.db import models

# 🚀 Modelo de Usuario extendido con campos adicionales
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    is_profesional = models.BooleanField(default=False)  # 🚀 Indica si es el dueño de la app

# 🚀 Modelo de Turno con validaciones de disponibilidad
class Turno(models.Model):
    profesional = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="turnos_profesional")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="turnos_usuario", null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    reservado = models.BooleanField(default=False)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.profesional.username}"


