# from email.message import EmailMessage
from django.conf import settings
from django.db import connection
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import check_password

from django.core.mail import EmailMessage

from rest_framework import generics, status
# from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import get_list_or_404, get_object_or_404
# from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives import hashes
import base64
# import json
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

from django.db.models import Q
from django.forms import model_to_dict

from django.core.files.storage import default_storage
import time
import cloudinary
import cloudinary.uploader
import cloudinary.utils
import cloudinary.api
from cloudinary.exceptions import Error as CloudinaryError
from datetime import datetime
from io import BytesIO

from app_django.models import Categoria, Subcategoria, Producto, Provincia, Localidad, Usuario, Cliente, Empleado, EstadoPedido, Pedido, Pedido_Producto, EstadoPago, MetodoPago
from app_django.models import Factura, Detalle_Envio, Talle, EstadoDevolucion, MotivoDevolucion, Devoluciones

from app_django.serializers import CategoriaSerializer, SubcategoriaSerializer, ProductoSerializer, ProvinciaSerializer, LocalidadSerializer, UsuarioSerializer
from app_django.serializers import ClienteSerializer, EmpleadoSerializer, EstadoPedidoSerializer, PedidoSerializer, Pedido_ProductoSerializer, EstadoPagoSerializer, MetodoPagoSerializer
from app_django.serializers import FacturaSerializer, Detalle_EnvioSerializer, TalleSerializer, EstadoDevolucionSerializer, MotivoDevolucionSerializer, DevolucionesSerializer

#SIRVE PARA ENVIAR EMAIL
import logging

logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)
#SIRVE PARA ENVIAR EMAIL

def home(request):
    try:
        return HttpResponse("Bienvenido a la página principal de la API")
    except Exception as e:
        logger.error(f"Error al renderizar la vista home: {str(e)}")
        return HttpResponse("Hubo un error", status=500)

# Create your views here.       
class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class SubcategoriaList(generics.ListCreateAPIView):
    queryset = Subcategoria.objects.all()
    serializer_class = SubcategoriaSerializer

class SubcategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subcategoria.objects.all()
    serializer_class = SubcategoriaSerializer

class ProductoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    parser_classes = (MultiPartParser, FormParser)  # Añade estos parsers para manejar archivos

    # def post(self, request, *args, **kwargs):
    #     # Crear un serializer con los datos recibidos
    #     serializer = self.get_serializer(data=request.data)
    #     print("Datos recibidos:", request.data)

    #     # Validar el serializer
    #     if not serializer.is_valid():
    #         print("Errores de validación:", serializer.errors)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     # Guardar el producto sin la imagen inicialmente
    #     producto = serializer.save()
    #     print("Producto creado sin imagen:", producto)

    #     # Manejo de la imagen (si está presente en los archivos)
    #     nueva_imagen = request.FILES.get('imagen')
    #     if nueva_imagen:
    #         if nueva_imagen.size == 0:
    #             print("La imagen está vacía.")
    #             return Response({'error': 'El archivo de imagen está vacío'}, status=status.HTTP_400_BAD_REQUEST)

    #         try:
    #             # Leer los bytes de la imagen para asegurarnos de que no estén vacíos
    #             nueva_imagen.seek(0)  # Asegurarse de que el puntero esté al inicio
    #             image_bytes = nueva_imagen.read()
    #             if not image_bytes:
    #                 print("Los bytes de la imagen están vacíos.")
    #                 return Response({'error': 'La imagen no se pudo leer correctamente'}, status=status.HTTP_400_BAD_REQUEST)
                
    #             # Generar un identificador único para la imagen
    #             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #             public_id = f'producto_{producto.id}_{timestamp}'
    #             print(f"Generando public_id para la imagen: {public_id}")

    #             # Subir la imagen a Cloudinary
    #             upload_result = cloudinary.uploader.upload(
    #                 image_bytes,
    #                 public_id=public_id,
    #                 overwrite=True,
    #                 folder='media'  # Opcional, especifica una carpeta
    #             )
    #             # Guardar la URL segura en el campo `imagen`
    #             producto.imagen = upload_result['secure_url'].split('/')[-1]
    #             producto.save()
    #             print("Imagen subida y asignada al producto:", producto.imagen)
    #         except cloudinary.exceptions.Error as e:
    #             print(f"Error al subir imagen a Cloudinary: {e}")
    #             return Response({'error': f'Error subiendo la imagen: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    #         except Exception as e:
    #             print(f"Error inesperado: {e}")
    #             return Response({'error': 'Error inesperado al subir la imagen'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #     # Retornar el producto creado con la imagen (si aplica)
    #     serializer = self.get_serializer(producto)  # Serializar el producto actualizado
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    parser_classes = (MultiPartParser, FormParser)  # Añade estos parsers para manejar archivos

    # def put(self, request, *args, **kwargs):
    #     try:
    #         # Intentamos obtener el producto que vamos a actualizar
    #         producto = self.get_object()
    #         print(f"Producto existente para actualizar: {producto}")
    #     except Producto.DoesNotExist:
    #         # Si no se encuentra el producto, devolvemos un error 404
    #         return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    #     # Usamos el serializer para validar y actualizar los datos del producto con los datos de la petición
    #     serializer = self.get_serializer(producto, data=request.data, partial=True)

    #      # Si los datos no son válidos, devolvemos los errores del serializer
    #     if not serializer.is_valid():
    #         print(f"Errores del serializer: {serializer.errors}")
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     # Manejo de la imagen subida (si existe una nueva imagen en la solicitud)
    #     nueva_imagen = request.FILES.get('imagen')
    #     if nueva_imagen:
    #         # Verificamos si el archivo de imagen está vacío
    #         if nueva_imagen.size == 0:
    #             print("El archivo está vacío.")
    #             return Response({'error': 'El archivo de imagen está vacío'}, status=status.HTTP_400_BAD_REQUEST)
    #         try:
    #             # Creamos un identificador único para la imagen, basado en la fecha y el ID del producto
    #             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #             public_id = f'producto_{producto.id}_{timestamp}'
    #             print(f"Generando public_id: {public_id}")

    #             # Subimos la imagen a Cloudinary, pasando el archivo y el identificador único
    #             upload_result = cloudinary.uploader.upload(
    #                 nueva_imagen,
    #                 public_id=public_id, # Usamos el identificador único para evitar colisiones
    #                 overwrite=True, # Permitir sobrescribir imágenes existentes con el mismo ID
    #                 folder='media' # Especificamos la carpeta en la que se almacenará la imagen
    #             )
    #             # Asignamos la URL segura de Cloudinary al campo imagen del producto
    #             producto.imagen = upload_result['secure_url'].split('/')[-1] 
    #             print(f"Imagen subida correctamente: {producto.imagen}")
    #         except cloudinary.exceptions.Error as e:
    #             # Si ocurre un error al subir la imagen, lo capturamos y devolvemos un mensaje de error
    #             print(f"Error al subir imagen a Cloudinary: {e}")
    #             return Response({'error': f'Error subiendo la imagen: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    #         except Exception as e:
    #              # Capturamos cualquier otro error inesperado y devolvemos un mensaje de error genérico
    #             print(f"Error inesperado: {e}")
    #             return Response({'error': 'Error inesperado al subir la imagen'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     elif 'imagen' in request.data and (not request.data['imagen'] or request.data['imagen'] == 'null'):
    #         # Si el campo de imagen está vacío o es 'null', no se realiza ninguna modificación en la imagen
    #         print("Campo 'imagen' vacío o null en el request. No se modifica la imagen.")

    #     # Guardamos los cambios del producto con los datos actualizados del serializer
    #     producto = serializer.save()

    #     # Devolvemos los datos actualizados del producto como respuesta
    #     return Response(serializer.data, status=status.HTTP_200_OK)
        
class ProvinciaList(generics.ListCreateAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer

class ProvinciaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer

class LocalidadList(generics.ListCreateAPIView):
    queryset = Localidad.objects.all()
    serializer_class = LocalidadSerializer

class LocalidadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Localidad.objects.all()
    serializer_class = LocalidadSerializer

class UsuarioList(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ClienteList(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
class EmpleadoList(generics.ListCreateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class EmpleadoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class EstadoPedidoList(generics.ListCreateAPIView):
    queryset = EstadoPedido.objects.all()
    serializer_class = EstadoPedidoSerializer

class EstadoPedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EstadoPedido.objects.all()
    serializer_class = EstadoPedidoSerializer
        
class PedidoList(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
        
class Pedido_ProductoList(generics.ListCreateAPIView):
    queryset = Pedido_Producto.objects.all()
    serializer_class = Pedido_ProductoSerializer

class Pedido_ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido_Producto.objects.all()
    serializer_class = Pedido_ProductoSerializer

class EstadoPagoList(generics.ListCreateAPIView):
    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer

class EstadoPagoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer

class MetodoPagoList(generics.ListCreateAPIView):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer

class MetodoPagoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer

class FacturaList(generics.ListCreateAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

class FacturaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

class Detalle_EnvioList(generics.ListCreateAPIView):
    queryset = Detalle_Envio.objects.all()
    serializer_class = Detalle_EnvioSerializer

class Detalle_EnvioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Detalle_Envio.objects.all()
    serializer_class = Detalle_EnvioSerializer

class TalleList(generics.ListCreateAPIView):
    queryset = Talle.objects.all()
    serializer_class = TalleSerializer

class TalleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Talle.objects.all()
    serializer_class = TalleSerializer

class EstadoDevolucionList(generics.ListCreateAPIView):
    queryset = EstadoDevolucion.objects.all()
    serializer_class = EstadoDevolucionSerializer

class EstadoDevolucionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EstadoDevolucion.objects.all()
    serializer_class = EstadoDevolucionSerializer

class MotivoDevolucionList(generics.ListCreateAPIView):
    queryset = MotivoDevolucion.objects.all()
    serializer_class = MotivoDevolucionSerializer

class MotivoDevolucionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MotivoDevolucion.objects.all()
    serializer_class = MotivoDevolucionSerializer

class DevolucionesList(generics.ListCreateAPIView):
    queryset = Devoluciones.objects.all()
    serializer_class = DevolucionesSerializer
    parser_classes = (MultiPartParser, FormParser)  # Añade estos parsers para manejar archivos

    # def post(self, request, *args, **kwargs):
    #     # Crear un serializer con los datos recibidos
    #     serializer = self.get_serializer(data=request.data)
    #     print("Datos recibidos:", request.data)

    #     # Validar el serializer
    #     if not serializer.is_valid():
    #         print("Errores de validación:", serializer.errors)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     print("Datos correctos")
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

class DevolucionesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Devoluciones.objects.all()
    serializer_class = DevolucionesSerializer
    parser_classes = (MultiPartParser, FormParser)  # Añade estos parsers para manejar archivos

# Archivos de clave pública y privada
PUBLIC_KEY_FILE = "public_key.pem"
PRIVATE_KEY_FILE = "private_key.pem"

# Esta función genera las claves si no existen
def generate_keys_if_not_exist():
    if not os.path.isfile(PUBLIC_KEY_FILE) or not os.path.isfile(PRIVATE_KEY_FILE):
        from .generate_keys import generate_keys
        generate_keys()

# Esta función devuelve la clave pública al cliente
def get_public_key(request):
    generate_keys_if_not_exist()
    with open(PUBLIC_KEY_FILE, "rb") as f:
        public_key = f.read()
    return JsonResponse({"public_key": public_key.decode('utf-8')})

# Esta función carga la clave privada desde el archivo
def load_private_key():
    with open(PRIVATE_KEY_FILE, "rb") as key_file:
        private_key = RSA.import_key(key_file.read())
    return private_key

# Esta función descifra un mensaje usando la clave privada
def decrypt_message(encrypted_message, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    decoded_data = base64.b64decode(encrypted_message)
    decrypted_message = cipher.decrypt(decoded_data)
    return decrypted_message.decode('utf-8')

# def decrypt_data(encrypted_data, private_key):
#     try:
#         print(f"Encrypted data: {encrypted_data}")
#         decoded_data = base64.b64decode(encrypted_data)
#         print(f"Decoded data: {decoded_data}")
        
#         decrypted_data = private_key.decrypt(
#             decoded_data,
#             padding.OAEP(
#                 mgf=padding.MGF1(algorithm=hashes.SHA256()),
#                 algorithm=hashes.SHA256(),
#                 label=None
#             )
#         )
#         print("Data successfully decrypted")
#         return decrypted_data.decode('utf-8')
#     except Exception as e:
#         print(f"Error decrypting data: {e}")
#         raise

# Vista para verificar las credenciales del usuario
@csrf_exempt
def verificar_credenciales(request):
    if request.method == 'GET':
        # Obtiene los datos cifrados desde la solicitud GET
        encrypted_email = request.GET.get('email')
        encrypted_password = request.GET.get('contrasenia')

        # Verifica que los datos cifrados estén presentes
        if not encrypted_email or not encrypted_password:
            return JsonResponse({'error': 'Missing email or password'}, status=400)
        
        # Debug prints para verificar los datos cifrados recibidos
        print("Encrypted Email (Base64):", encrypted_email)
        print("Encrypted Password (Base64):", encrypted_password)

        private_key = load_private_key()

        try:
            # Descifra los datos cifrados
            decrypted_email = decrypt_message(encrypted_email, private_key)
            decrypted_password = decrypt_message(encrypted_password, private_key)
        except Exception as e:
            return JsonResponse({'error': 'Decryption failed', 'message': str(e)}, status=400)
        
        # Debug prints para verificar los datos descifrados
        print("Decrypted Email:", decrypted_email)
        print("Decrypted Password:", decrypted_password)

        # Verifica el email y la contraseña con la base de datos
        try:
            usuario = Usuario.objects.get(email=decrypted_email)
            
            if usuario.activo == 2:
                return JsonResponse({"detalle": "El usuario está bloqueado"}, status=403)

            if check_password(decrypted_password, usuario.contrasenia):
                usuario_data = {
                    'id': usuario.id,
                    'email': usuario.email,
                    'activo': usuario.activo,
                }
                usuario.cant_intentos = 0
                usuario.save()
                return JsonResponse(usuario_data)
            else:
                usuario.cant_intentos += 1
                if usuario.cant_intentos < 3:
                    usuario.save()
                    return JsonResponse({"detalle": "Email o Contraseña incorrectos"}, status=401)
                if usuario.cant_intentos >= 3:
                    usuario.activo = 2
                    usuario.save()
                    return JsonResponse({"detalle": "Credenciales inválidas, usuario bloqueado"}, status=403)
        except Usuario.DoesNotExist:
            return JsonResponse({"detalle": "Usuario no encontrado"}, status=404)
    else:
        return JsonResponse({"detalle": "Método no permitido"}, status=405)
    
def localidades_por_provincia(request, provincia_id):
    localidades = get_list_or_404(Localidad, provincia_id=provincia_id)
    localidades_data = [{'id': loc.id, 'descripcion': loc.descripcion} for loc in localidades]
    return JsonResponse(localidades_data, safe=False)

# Función de vista para obtener productos activos por nombre o descripcion
@api_view(['GET'])
def buscar_productos(request):
    termino = request.GET.get('busqueda', '')
    productos = Producto.objects.filter(
        Q(nombre__icontains=termino) | Q(descripcion__icontains=termino),
        activo=1
    )
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
# def buscar_productos(request):
#     query = request.GET.get('busqueda', '')
#     productos = Producto.objects.filter(
#         Q(nombre__icontains=termino) | Q(descripcion__icontains=termino),
#         activo=1
#     )
#     resultados = [
#         {
#             'id': producto.id,
#             'nombre': producto.nombre,
#             'descripcion': producto.descripcion,
#             'talle': producto.talle,
#             'color': producto.color,
#             'precio': producto.precio,
#             'cantidad': producto.cantidad,
#             'cantidad_disponible': producto.cantidad_disponible,
#             'cantidad_limite': producto.cantidad_limite,
#             'imagen': producto.imagen.url if producto.imagen else None,
#             'observaciones': producto.observaciones,
#         }
#     for producto in productos]
    
#     return JsonResponse(resultados, safe=False)

# Función de vista para obtener categorías activas
def categorias_activas(request):
    categorias = Categoria.objects.filter(activo=True)
    serializer = CategoriaSerializer(categorias, many=True)
    return JsonResponse(serializer.data, safe=False)

# Función de vista para obtener subcategorías activas por categoría
def subcategorias_activas_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    subcategorias = Subcategoria.objects.filter(categoria=categoria, activo=True)
    serializer = SubcategoriaSerializer(subcategorias, many=True)
    return JsonResponse(serializer.data, safe=False)

# def productos_por_categoria(request, categoria_id):
#     productos = Producto.objects.filter(categoria_id=categoria_id, activo=1)
#     data = list(productos.values())
#     return JsonResponse(data, safe=False)

# def productos_por_subcategoria(request, subcategoria_id):
#     productos = Producto.objects.filter(subcategoria_id=subcategoria_id, activo=1)
#     data = list(productos.values())
#     return JsonResponse(data, safe=False)

# Función de vista para obtener los Productos segun la Categoría seleccionada
@api_view(['GET'])
def productos_por_categoria(request, categoria_id):
    try: 
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        productos = Producto.objects.filter(categoria=categoria, activo = 1)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Categoria.DoesNotExist:
        return Response({'error': 'Categoria no encontrada'}, status=status.HTTP_404_NOT_FOUND)

# Función de vista para obtener los Productos segun la Subcategoría seleccionada
@api_view(['GET'])
def productos_por_subcategoria(request, subcategoria_id):
    try:
        subcategoria = get_object_or_404(Subcategoria, pk=subcategoria_id)
        productos = Producto.objects.filter(subcategoria=subcategoria, activo = 1)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Subcategoria.DoesNotExist:
        return Response({'error': 'Subcategoria no encontrada'}, status=status.HTTP_404_NOT_FOUND)

# Función de vista para obtener productos activos
@api_view(['GET'])
def productos_activos(request):
    productos = Producto.objects.filter(activo=1)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

# Función de vista para obtener productos activos segun estos distintos tipos de filtros
@api_view(['GET'])
def filtrar_productos(request):
    nombre = request.GET.get('nombre', '')
    descripcion = request.GET.get('descripcion', '')
    categoria_id = request.GET.get('categoria', '')
    subcategoria_id = request.GET.get('subcategoria', '')
    precio_desde = request.GET.get('precio_desde', '')
    precio_hasta = request.GET.get('precio_hasta', '')
    color = request.GET.get('color', '')
    talle = request.GET.get('talle', '')

    # Filtramos para que esten solo los Productos Activos
    productos = Producto.objects.filter(activo=1)

    # Construyendo la consulta de filtro
    # Filtro de nombre
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    # Filtro de descripcion
    if descripcion:
        productos = productos.filter(descripcion__icontains=descripcion)
    # Filtro de categoria
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    # Filtro de subcategoria
    if subcategoria_id:
        productos = productos.filter(subcategoria_id=subcategoria_id)
    # Filtro de precio desde (mayor o igual a)
    if precio_desde:
        productos = productos.filter(precio__gte=precio_desde)
    # Filtro de precio hasta (menor o igual a)
    if precio_hasta:
        productos = productos.filter(precio__lte=precio_hasta)
    # Filtro de color
    if color:
        productos = productos.filter(color=color)
    # Filtro de talle
    if talle:
        productos = productos.filter(talle=talle)

    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

# Función de vista para obtener productos activos
# def productos_activos(request, producto_id):
#     producto = Producto.objects.filter(activo=1, id=producto_id)
#     productos = productos.filter(id=producto_id)
#     data = list(productos.values())
#     return JsonResponse(data, safe=False)

# Función de vista para obtener un producto activo por ID
def productos_activos_por_id(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=1)

    # Producto MODIFICADO
    producto_data = {
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'talle': producto.talle,
        'color': producto.color,
        # 'categoria': producto.categoria.nombre if producto.categoria else None, #Pasar el Nombre de la Categoria en vez del numero
        'categoria': producto.categoria.id,
        # 'subcategoria': producto.subcategoria.nombre if producto.subcategoria else None, #Pasar el Nombre de la Subcategoria en vez del numero
        'subcategoria': producto.subcategoria.id if producto.subcategoria else None, #Pasar el Nombre de la Subcategoria en vez del numero
        # 'subcategoria': producto.subcategoria.id,
        'precio': producto.precio,
        'cantidad': producto.cantidad,
        'cantidad_disponible': producto.cantidad_disponible,
        'cantidad_limite': producto.cantidad_limite,
        'imagen': producto.imagen.url if producto.imagen else None,  # Accede a la URL de la imagen
        'observaciones': producto.observaciones,
        'activo': producto.activo
    }
    return JsonResponse(producto_data)

# # Función de vista para obtener un producto activo por ID
# def usuarios_sin_contraseña():
#     usuario = get_object_or_404(Usuario)

#     # Producto MODIFICADO
#     usuario_data = {
#         'email': usuario.id,
#         # 'contrasenia': usuario.contrasenia,
#         'cant_intentos': usuario.cant_intentos,
#         'activo': usuario.activo
#     }
#     return JsonResponse(usuario_data)


# Función de vista para obtener un producto activo por ID
@api_view(['POST'])
def cargar_carrito_de_cliente(request, cliente_id):    
    # Verificar si el cliente ya tiene un pedido activo (estado = "carrito")
    try:
        elPedido = Pedido.objects.get(cliente=cliente_id, estado__estado="carrito")
    except Pedido.DoesNotExist:
        # Crear pedido si no existe
        elCliente = Cliente.objects.get(id=cliente_id)
        estado_carrito = EstadoPedido.objects.get(estado="carrito")  # Buscar estado "carrito"

        elPedido = Pedido.objects.create(
            cliente= elCliente,
            estado= estado_carrito, # Asignar el estado como instanci
            fecha_pactada= None,  # O asigna un valor por defecto
            fecha_entregada= None,  # O asigna un valor por defecto
            total= 0.00  # El total comenzará en 0
        )

    # Obtener producto y cantidad desde el request
    producto_id = request.data.get('producto_id')
    cantidad = request.data.get('cantidad')
    elProducto = Producto.objects.get(id=producto_id)

    # Crear o actualizar Pedido_Producto
    sub_total = elProducto.precio * int(cantidad)
    pedido_producto, created = Pedido_Producto.objects.get_or_create(
        pedido= elPedido,
        producto= elProducto,
        defaults={
            'cantidad': cantidad,
            'sub_total': sub_total
        }
    )

    if not created:
        # Si ya existía la relación entre pedido y producto, actualizar cantidad y totales
        pedido_producto.cantidad += int(cantidad)
        pedido_producto.sub_total = elProducto.precio * pedido_producto.cantidad
        pedido_producto.save()
    
    # Actualizar el total del pedido sumando el total de todos los productos en el pedido
    total_pedido = sum(p.sub_total for p in Pedido_Producto.objects.filter(pedido=elPedido))
    elPedido.total = total_pedido
    elPedido.save()

    return Response(PedidoSerializer(elPedido).data, status=status.HTTP_200_OK)

# def pedido_carrito_por_cliente(request, cliente_id):
#     pedido = get_object_or_404(Pedido, cliente=cliente_id, estado=1)

#     # Producto MODIFICADO
#     pedido_data = {
#         'id': pedido.id,
#         'cliente': pedido.cliente,
#         'fecha_creacion': pedido.fecha_creacion,
#         'fecha_pactada': pedido.fecha_pactada,
#         'fecha_entregada': pedido.fecha_entregada,
#         'estado': pedido.estado,
#         'total': pedido.total,
#         'observaciones': pedido.observaciones
#     }
#     return JsonResponse(pedido_data)
    
#     # Verificar si el cliente ya tiene un pedido activo (con estado 0)
#     # cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)
#     # fecha_creacion = models.DateField(auto_now=True)
#     # fecha_pactada = models.DateField()
#     # fecha_entregada = models.DateField()
#     # estado = models.ForeignKey(Estado, null=True, on_delete=models.SET_NULL)
#     # total = models.DecimalField(max_digits=10, decimal_places=2)
#     # observaciones = models.TextField(blank=True, max_length=200)

@api_view(['GET'])
def pedido_carrito_por_cliente(request, cliente_id):
    try:
        pedido = Pedido.objects.get(cliente=cliente_id, estado__estado__iexact="carrito")
    except Pedido.DoesNotExist:
        return Response({"error": "Pedido no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PedidoSerializer(pedido)
    return Response(serializer.data)

# Función de vista para obtener productos activos
def productos_por_pedido(request, pedido_id):
    pedido_productos = Pedido_Producto.objects.filter(pedido=pedido_id)
    data = list(pedido_productos.values())
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def pedido_productos_carrito_por_cliente(request, cliente_id):
    estado_carrito = EstadoPedido.objects.get(estado='carrito')
    # pedido = Pedido.objects.filter(cliente_id=cliente_id, estado=estado_carrito).first()
    
    try:
        pedido = Pedido.objects.filter(cliente_id=cliente_id, estado=estado_carrito).first()
    except Pedido.DoesNotExist:
        return Response({"error": "Pedido no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    # if not pedido:
    #     return Response({"error": "No hay productos en el carrito."}, status=404)

    productos_carrito = Pedido_Producto.objects.filter(pedido=pedido)
    serializer = Pedido_ProductoSerializer(productos_carrito, many=True)
    return Response(serializer.data, status=200)
    # try:
    #     estado_carrito = EstadoPedido.objects.get(estado='carrito')
    #     pedido = Pedido.objects.filter(cliente_id=cliente_id, estado=estado_carrito).first()
        
    #     if not pedido:
    #         return Response({"detail": "No hay productos en el carrito."}, status=404)

    #     productos_carrito = Pedido_Producto.objects.filter(pedido=pedido)
    #     serializer = Pedido_ProductoSerializer(productos_carrito, many=True)
    #     return Response(serializer.data, status=200)
    # except EstadoPedido.DoesNotExist:
    #     return Response({"detail": "Estado 'carrito' no encontrado."}, status=400)

@api_view(['POST'])
def verificar_contrasenia_actual(request, usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
        contrasenia_actual = request.data.get('contrasenia', '')
        
        print("Contraseña Actual:", contrasenia_actual)

        # Solo verifica la contraseña actual si se proporciona
        if contrasenia_actual and check_password(contrasenia_actual, usuario.contrasenia):
            return Response({'valida': True}, status=status.HTTP_200_OK) # La contraseña proporciona coincide con la contraseña actual
        elif contrasenia_actual:
            # return Response({'valida': False}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'valida': False}) # La contraseña proporciona NO coincide con la contraseña actual
        else:
            # return Response({'valida': True}, status=status.HTTP_200_OK)  # No se requiere verificación si no se proporciona contraseña actual
            return Response({'valida': True})  # No se requiere verificación porque no se proporciono la contraseña actual
    except Usuario.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def contacto_enviar_email(request):
    nombre = request.data.get('name')
    email = request.data.get('email')  # El email del remitente (quien llena el formulario)
    sujeto = request.data.get('subject')
    mensaje = request.data.get('message')

    print("nombre: ", nombre)
    print("email: ", email)
    print("sujeto: ", sujeto)
    print("mensaje: ", mensaje)

    # Crear el correo
    email_message = EmailMessage(
        subject=f'{sujeto} - {nombre}',  # Asunto que incluye el nombre de quien escribe
        body=f'Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}',  # Cuerpo del mensaje
        from_email='marceloprueba260@gmail.com',  # Desde tu email
        to=['marcelop639@gmail.com'],  # El destinatario del correo
        reply_to=[email]  # Email de quien llena el formulario
    )

    try:
        email_message.send(fail_silently=False)
        logger.info("Email enviado exitosamente")
        return Response({"message": "Email enviado exitosamente."}, status=200)
    except Exception as e:
        logger.error(f"Error al enviar el email: {e}")
        return Response({"error": "Error al enviar el email."}, status=500)

@api_view(['POST'])
def informe_pedidos_fecha_desde_hasta_raw(request):
    desde = request.data.get('desde')
    hasta = request.data.get('hasta')

    query = '''
        SELECT 
            p.fecha_creacion,
            p.id AS pedido_id,
            SUM(pp.cantidad) AS total_cantidad,
            p.total
        FROM 
            app_django_pedido p
        JOIN 
            app_django_pedido_producto pp ON p.id = pp.pedido_id
        WHERE 
            p.fecha_creacion BETWEEN %s AND %s
        GROUP BY 
            p.fecha_creacion, p.id, p.total
        ORDER BY 
            p.fecha_creacion;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query, [desde, hasta])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results = []
        for row in rows:
            row_dict = {}
            for idx, col in enumerate(columns):
                row_dict[col] = row[idx]
            results.append(row_dict)

    return Response(results)

@api_view(['POST'])
def informe_devoluciones_fecha_desde_hasta_raw(request):
    fecha_inicio = request.data.get('fecha_inicio')
    fecha_fin = request.data.get('fecha_fin')
    motivo_id = request.data.get('motivo_id')  # Puede ser opcional
    estado_id = request.data.get('estado_id')
    # print("motivo: ", motivo_id)
    # print("estado: ", estado_id)

    # Validar que las fechas sean proporcionadas
    if not (fecha_inicio and fecha_fin):
        return Response({
            "error": "Los campos 'fecha_inicio' y 'fecha_fin' son obligatorios."
        }, status=400)

    # Construir la consulta base
    query = '''
        SELECT 
            d.fecha_solicitud AS fecha_solicitud,
            d.pedido_id AS nro_pedido,
            md.nombre AS motivo,
            ed.nombre AS estado,
            d.observacion AS observaciones,
            p.nombre AS nombre_producto,
            p.precio AS precio_producto,
            d.cantidad AS cantidad_devuelta,
            (d.cantidad * p.precio) AS valor_total
        FROM 
            app_django_devoluciones d
        INNER JOIN 
            app_django_estadodevolucion ed ON d.estado_id = ed.id
        INNER JOIN 
            app_django_motivodevolucion md ON d.motivo_id = md.id
        INNER JOIN 
            app_django_producto p ON d.producto_id = p.id
        WHERE 
            d.fecha_solicitud BETWEEN %s AND %s

    '''

    # Agregar la condición opcional para motivo_id
    params = [fecha_inicio, fecha_fin]
    if motivo_id:
        print("motivoif: ", motivo_id)
        query += " AND d.motivo_id = %s"
        params.append(motivo_id)
    
    if estado_id:
        print("estadoif: ", estado_id)
        query += " AND d.estado_id = %s"
        params.append(estado_id)

    # Ejecutar la consulta y procesar los resultados
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        results = [
            {
                "fecha_solicitud": row[0],
                "nro_pedido": row[1],
                "motivo": row[2],
                "estado": row[3],
                "observaciones": row[4],
                "nombre_producto": row[5],
                "precio_producto": row[6],
                "cantidad_devuelta": row[7],
                "valor_total": row[8],
            }
            for row in rows
        ]

    return Response(results)

@api_view(['POST']) # informes
def informe_menores_ventas_fecha_desde_hasta_raw(request):
    # print("Llamada a la API")
    desde = request.data.get('desde')
    hasta = request.data.get('hasta')

    query = '''
        WITH ventas AS (
            SELECT 
                pr.id AS producto_id, 
                pr.nombre AS producto_nombre,
                COALESCE(SUM(pp.cantidad), 0) AS total_vendido  
            FROM 
                app_django_producto pr
            LEFT JOIN 
                app_django_pedido_producto pp ON pr.id = pp.producto_id
            LEFT JOIN 
                app_django_pedido p ON pp.pedido_id = p.id
            WHERE 
                p.fecha_creacion BETWEEN %s AND %s OR p.fecha_creacion IS NULL
            GROUP BY 
                pr.id, pr.nombre
        ),
        promedio_ventas AS (
            SELECT AVG(total_vendido) AS promedio FROM ventas
        )
        SELECT v.*
        FROM ventas v, promedio_ventas p
        WHERE v.total_vendido < p.promedio
        ORDER BY v.total_vendido ASC;


            '''
        # usar coalesce para mostrar 0 en vez de null

    with connection.cursor() as cursor:
        cursor.execute(query, [desde, hasta])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results = []
        for row in rows:
            row_dict = {}
            for idx, col in enumerate(columns):
                row_dict[col] = row[idx]
            results.append(row_dict)

    return Response(results)

@api_view(['POST']) # informes
def informe_mayores_ventas_fecha_desde_hasta_raw(request):
    # print("Llamada a la API")
    desde = request.data.get('desde')
    hasta = request.data.get('hasta')

    query = '''
        WITH ventas AS (
            SELECT 
                pr.id AS producto_id, 
                pr.nombre AS producto_nombre,
                COALESCE(SUM(pp.cantidad), 0) AS total_vendido  
            FROM 
                app_django_producto pr
            LEFT JOIN 
                app_django_pedido_producto pp ON pr.id = pp.producto_id
            LEFT JOIN 
                app_django_pedido p ON pp.pedido_id = p.id
            WHERE 
                p.fecha_creacion BETWEEN %s AND %s OR p.fecha_creacion IS NULL
            GROUP BY 
                pr.id, pr.nombre
        ),
        promedio_ventas AS (
            SELECT AVG(total_vendido) AS promedio FROM ventas
        )
        SELECT v.*
        FROM ventas v, promedio_ventas p
        WHERE v.total_vendido > p.promedio
        ORDER BY v.total_vendido ASC;


            '''
        # usar coalesce para mostrar 0 en vez de null

    with connection.cursor() as cursor:
        cursor.execute(query, [desde, hasta])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results = []
        for row in rows:
            row_dict = {}
            for idx, col in enumerate(columns):
                row_dict[col] = row[idx]
            results.append(row_dict)

    return Response(results)

@api_view(['POST']) # informes
def informe_clientes_destacados_fecha_desde_hasta_raw(request):
    # print("Llamada a la API")
    desde = request.data.get('desde')
    hasta = request.data.get('hasta')

    query = '''
        SELECT 
            c.id AS cliente_id,
            c.nombre || ' ' || c.apellido  AS cliente_nombre,
            COALESCE(SUM(p.total), 0) AS total_compras,
            COALESCE(SUM(pp.cantidad), 0) AS total_articulos
        FROM 
            app_django_cliente c
        LEFT JOIN 
            app_django_pedido p ON c.id = p.cliente_id
        LEFT JOIN 
            app_django_pedido_producto pp ON p.id = pp.pedido_id
        WHERE 
            (p.fecha_creacion >= %s AND p.fecha_creacion <= %s)
        GROUP BY 
            c.id, c.nombre
        ORDER BY 
            total_compras DESC;

            '''
        # usar coalesce para mostrar 0 en vez de null

    with connection.cursor() as cursor:
        cursor.execute(query, [desde, hasta])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results = []
        for row in rows:
            row_dict = {}
            for idx, col in enumerate(columns):
                row_dict[col] = row[idx]
            results.append(row_dict)

    return Response(results)

@api_view(['POST'])
def devoluciones_pedidos_cliente(request):
    cliente_id = request.data.get('cliente_id')

    if not cliente_id:
        return Response({"error": "El campo 'cliente_id' es obligatorio."}, status=400)

    query = '''
        SELECT 
            p.id AS pedido_id,
            p.fecha_creacion || ' - Nº: ' || p.id AS pedido_info
        FROM 
            app_django_pedido p
        JOIN 
            app_django_cliente c ON p.cliente_id = c.id
        WHERE 
            c.id = %s AND p.estado_id = 5;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query, [cliente_id])
        rows = cursor.fetchall()
        # Obtenemos los nombres de las columnas automáticamente
        columns = [col[0] for col in cursor.description]
        # Construimos el resultado dinámicamente
        results = [
            {columns[idx]: value for idx, value in enumerate(row)}
            for row in rows
        ]

    return Response(results)

@api_view(['POST'])
def devoluciones_productos_pedido(request):
    pedido_id = request.data.get('pedido_id')

    if not pedido_id:
        return Response({"error": "El campo 'pedido_id' es obligatorio."}, status=400)

    query = '''
        SELECT 
            pp.id AS pedido_producto_id,
            pp.producto_id AS producto_id,
            (pp.cantidad - COALESCE(
                (SELECT SUM(d.cantidad) 
                 FROM app_django_devoluciones d 
                 WHERE d.pedido_id = pp.pedido_id AND d.producto_id = pp.producto_id AND d.estado_id <> 3), 
                0)
            ) AS cantidad_disponible,
            prod.nombre || ' | Cantidad: ' || 
            (pp.cantidad - COALESCE(
                (SELECT SUM(d.cantidad) 
                 FROM app_django_devoluciones d 
                 WHERE d.pedido_id = pp.pedido_id AND d.producto_id = pp.producto_id AND d.estado_id <> 3), 
                0)
            ) AS producto_info
        FROM 
            app_django_pedido_producto pp
        INNER JOIN 
            app_django_producto prod ON pp.producto_id = prod.id
        WHERE 
            pp.pedido_id = %s;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query, [pedido_id])
        rows = cursor.fetchall()
        # Obtenemos los nombres de las columnas automáticamente
        columns = [col[0] for col in cursor.description]
        # Construimos el resultado dinámicamente
        results = [
            {columns[idx]: value for idx, value in enumerate(row)}
            for row in rows
        ]

    return Response(results)

# def obtener_devoluciones(request):
#     devoluciones = Devoluciones.objects.select_related('producto').all()
#     resultado = []
#     for devolucion in devoluciones:
#         resultado.append({
#             'id': devolucion.id,
#             'pedido': devolucion.pedido.id if devolucion.pedido else None,
#             'producto_nombre': devolucion.producto.nombre if devolucion.producto else None,
#             'producto_imagen': devolucion.producto.imagen.url if devolucion.producto and devolucion.producto.imagen else None,
#             'motivo': devolucion.motivo.nombre if devolucion.motivo else None,
#             'estado': devolucion.estado.nombre if devolucion.estado else None,
#             'cantidad': devolucion.cantidad,
#             'observacion': devolucion.observacion,
#             'fecha_solicitud': devolucion.fecha_solicitud,
#         })
#     return JsonResponse(resultado, safe=False)

def listado_devoluciones_por_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    # devoluciones = Devoluciones.objects.filter(pedido__cliente=cliente).select_related('producto', 'motivo', 'estado')
    devoluciones = (
        Devoluciones.objects
        .filter(pedido__cliente=cliente)
        .select_related('pedido','producto', 'motivo', 'estado')
        .order_by('-id')  # Ordenar por ID en orden descendente
    )

    resultado = [
        {
            'id': devolucion.id,
            'pedido': devolucion.pedido.id,
            'fecha_solicitud': devolucion.fecha_solicitud,
            'producto': {
                'id': devolucion.producto.id,
                'nombre': devolucion.producto.nombre,
                'imagen': devolucion.producto.imagen.url if devolucion.producto.imagen else None
            },
            'motivo': devolucion.motivo.nombre if devolucion.motivo else None,
            'estado': devolucion.estado.nombre if devolucion.estado else None,
            'cantidad': devolucion.cantidad,
            'imagen': devolucion.imagen.url if devolucion.imagen else None,
            'observacion': devolucion.observacion
        }
        for devolucion in devoluciones
    ]

    return JsonResponse(resultado, safe=False)
    # return JsonResponse({'devoluciones': resultado}, safe=False)

@csrf_exempt  # Si estás trabajando con formularios POST sin autenticar
def get_cloudinary_signature(request):
    timestamp = int(time.time())  # Hora actual en formato Unix

    # Definir los parámetros que se van a firmar
    params_to_sign = {
        "timestamp": timestamp,
        "upload_preset": "ml_default",  # Aquí usas el nombre de tu preset
    }

    # Generamos la firma usando tu api_secret
    signature = cloudinary.utils.api_sign_request(params_to_sign, settings.CLOUDINARY_API_SECRET)

    # Devolvemos la firma junto con el api_key y el timestamp
    return JsonResponse({
        "signature": signature,
        "api_key": settings.CLOUDINARY_API_KEY,
        "timestamp": timestamp
    })