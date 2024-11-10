#!/bin/bash

set -x  # Muestra cada comando antes de ejecutarlo

echo "Iniciando script..."

# Establecer el puerto si no está definido
export PORT=${PORT:-8000}

# Navegar al directorio del proyecto donde se encuentra manage.py
cd ./proyecto_django/proyecto_django || { echo "Error al cambiar de directorio"; exit 1; }
echo "Cambiado al directorio: $(pwd)"

# Realizar migraciones de base de datos
echo "Realizando migraciones de base de datos..."
python manage.py migrate || { echo "Error al ejecutar migraciones"; exit 1; }

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput || { echo "Error al recopilar archivos estáticos"; exit 1; }

# # Iniciar el servidor de desarrollo de Django
# echo "Iniciando el servidor de desarrollo..."
# exec python manage.py runserver 0.0.0.0:${PORT} || { echo "Error al iniciar el servidor"; exit 1; }

# Iniciar el servidor con Waitress
echo "Iniciando el servidor con Waitress..."
exec waitress-serve --port=$PORT proyecto_django.wsgi:application || { echo "Error al iniciar el servidor"; exit 1; }

echo "Script finalizado."