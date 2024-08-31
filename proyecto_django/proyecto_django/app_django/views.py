from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import check_password

from rest_framework import generics, status
# from rest_framework.views import APIView
from rest_framework.response import Response

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

from app_django.models import Categoria, Subcategoria, Producto, Provincia, Localidad, Usuario, Cliente, Empleado, Estado, Pedido, Pedido_Producto, Factura, Detalle_Envio

from app_django.serializers import CategoriaSerializer, SubcategoriaSerializer, ProductoSerializer, ProvinciaSerializer, LocalidadSerializer, UsuarioSerializer
from app_django.serializers import ClienteSerializer, EmpleadoSerializer, EstadoSerializer, PedidoSerializer, Pedido_ProductoSerializer, FacturaSerializer, Detalle_EnvioSerializer
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

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
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

class EstadoList(generics.ListCreateAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class EstadoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
        
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
def productos_activos(request):
    productos = Producto.objects.filter(activo=1)
    data = list(productos.values())
    return JsonResponse(data, safe=False)

# Función de vista para obtener productos activos segun estos distintos tipos de filtros
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

    # Serializar los productos a formato JSON
    productos_json = list(productos.values())
    # Retornar los productos en formato JSON
    return JsonResponse(productos_json, safe=False)

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

# Función de vista para obtener un producto activo por ID
def usuarios_sin_contraseña():
    usuario = get_object_or_404(Usuario)

    # Producto MODIFICADO
    usuario_data = {
        'email': usuario.id,
        # 'contrasenia': usuario.contrasenia,
        'cant_intentos': usuario.cant_intentos,
        'activo': usuario.activo
    }
    return JsonResponse(usuario_data)

