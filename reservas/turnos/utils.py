from django.core.mail import send_mail
from django.conf import settings

def enviar_notificacion(destinatario, asunto, mensaje):
    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,  # 🚀 Usamos la configuración de Django
        [destinatario],
        fail_silently=False,
    )
