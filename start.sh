#!/bin/bash

# Navegar al directorio donde se encuentra manage.py
cd /app/proyecto_django/proyecto_django

# Realizar migraciones de base de datos
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar el servidor usando Gunicorn
exec gunicorn proyecto_django.wsgi:application --bind 0.0.0.0:$PORT --log-file -