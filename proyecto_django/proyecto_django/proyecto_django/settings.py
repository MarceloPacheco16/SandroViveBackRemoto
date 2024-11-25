"""
Django settings for proyecto_django project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

#Para usar una Base de Datos de PostgreSQL en vez de Sqlite3 (Recomendado - estado: Incompleto)
# import dj_database_url

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.getenv('DEBUG', 'False') == 'True'
print(f"DEBUG: {DEBUG}")


# ESTO NO ES NECESARIO EN PRODUCCION (Variables de Entorno en Plataforma de Railway)
if DEBUG:  # Solo carga .env en desarrollo
    from dotenv import load_dotenv
    load_dotenv()
# ESTO NO ES NECESARIO EN PRODUCCION (Variables de Entorno en Plataforma de Railway)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-i)o17+#qxfu2@hi8ngen8fw1)e+2x5c^p*jl(7!pa$2635qt-a'
SECRET_KEY = os.getenv('SECRET_KEY')
print(f"SECRET_KEY: {SECRET_KEY}")

# # ALLOWED_HOSTS = []
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '')  # Establecer un valor predeterminado vacío
if ALLOWED_HOSTS:  # Si la variable está vacía, evitamos el split
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')
else:
    ALLOWED_HOSTS = []

# Depuración: Imprimir el valor de ALLOWED_HOSTS para verificar si se carga correctamente
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")


# import cloudinary

# Configuración de Cloudinary
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

# Configuración para organizar archivos estáticos
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
    'STATIC_IMAGES_FOLDER': 'staticfiles',  # Carpeta raíz para archivos estáticos
}

# # Configuración de Cloudinary
# cloudinary.config(
#     cloud_name=CLOUDINARY_CLOUD_NAME,
#     api_key=CLOUDINARY_API_KEY,
#     api_secret=CLOUDINARY_API_SECRET,
# )

# Configuración de Cloudinary como almacenamiento de archivos
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Usando Cloudinary para los archivos estáticos
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'


# Application definition

INSTALLED_APPS = [
    'app_django',
    'rest_framework',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Configuración de REST Framework
REST_FRAMEWORK = {
    # Especifica el esquema de autenticación que deseas utilizar
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    # Especifica el esquema de permisos que deseas utilizar
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Permitir acceso a todos los usuarios
    ],
    # Agrega otros ajustes que consideres necesarios
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  # Control de la tasa de solicitudes para usuarios anónimos
        'rest_framework.throttling.UserRateThrottle',  # Control de la tasa de solicitudes para usuarios autenticados
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',  # 100 solicitudes por día para anónimos
        'user': '1000/day',  # 1000 solicitudes por día para usuarios autenticados
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Renderiza respuestas en formato JSON
        'rest_framework.renderers.BrowsableAPIRenderer',  # Agregar el renderizador de navegador
    ],
    'DEFAULT_TEMPLATE_PACK': 'rest_framework/horizontal',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # Permite analizar solicitudes en formato JSON
    ],
}

# Configuración de CORS para permitir el origen de Angular
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:4200",
    "https://sandro-vive-front-remoto.vercel.app",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "https://sandro-vive-front-remoto.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Añadir WhiteNoise aquí
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proyecto_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proyecto_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# #Para usar una Base de Datos de PostgreSQL en vez de Sqlite3 (Recomendado - estado: Incompleto)
# # Configuración para entorno de producción
# if not DEBUG:  # Si DEBUG es False, se considera que estamos en producción
#     DATABASES['default'] = dj_database_url.config(
#         default=os.getenv('DATABASE_URL')
#     )
# #Para usar una Base de Datos de PostgreSQL en vez de Sqlite3 (Recomendado - estado: Incompleto)


# Configuración de email
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'marceloprueba260@gmail.com'  # Tu email
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Contraseña del email
DEFAULT_FROM_EMAIL = 'marceloprueba260@gmail.com'  # Mismo email por defecto

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Usando Whitenoise para servir archivos estáticos locales en desarrollo
# Esto solo afectará a los archivos estáticos locales, no los de Cloudinary
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')