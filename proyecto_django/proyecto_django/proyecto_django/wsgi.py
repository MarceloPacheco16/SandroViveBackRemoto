"""
WSGI config for proyecto_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from waitress import serve

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_django.settings')

application = get_wsgi_application()

# Usar Waitress para servir la aplicación en producción
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Usa el puerto de Railway o 8000 por defecto
    print(f"Servidor arrancado en el puerto: {port}")  # Log para confirmar el puerto
    serve(application, host='0.0.0.0', port=port)