from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import check_password

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

from app_django.models import Categoria, Subcategoria, Producto, Provincia, Localidad, Usuario, Cliente, Empleado, Estado, Pedido, Pedido_Producto, Factura, Detalle_Envio, Talle

from app_django.serializers import CategoriaSerializer, SubcategoriaSerializer, ProductoSerializer, ProvinciaSerializer, LocalidadSerializer, UsuarioSerializer
from app_django.serializers import ClienteSerializer, EmpleadoSerializer, EstadoSerializer, PedidoSerializer, Pedido_ProductoSerializer, FacturaSerializer, Detalle_EnvioSerializer
from app_django.serializers import TalleSerializer
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

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    parser_classes = (MultiPartParser, FormParser)  # Añade estos parsers para manejar archivos
    
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

class TalleList(generics.ListCreateAPIView):
    queryset = Talle.objects.all()
    serializer_class = TalleSerializer

class TalleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Talle.objects.all()
    serializer_class = TalleSerializer

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
        elPedido = Pedido.objects.get(cliente=cliente_id, estado__tipo_estado="carrito")
    except Pedido.DoesNotExist:
        # Crear pedido si no existe
        elCliente = Cliente.objects.get(id=cliente_id)
        estado_carrito = Estado.objects.get(tipo_estado="carrito")  # Buscar estado "carrito"

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
        pedido = Pedido.objects.get(cliente=cliente_id, estado__tipo_estado="carrito")
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
def productos_carrito(request, cliente_id):
    try:
        estado_carrito = Estado.objects.get(tipo_estado='carrito')
        pedido = Pedido.objects.filter(cliente_id=cliente_id, estado=estado_carrito).first()
        
        if not pedido:
            return Response({"detail": "No hay productos en el carrito."}, status=404)

        productos_carrito = Pedido_Producto.objects.filter(pedido=pedido)
        serializer = Pedido_ProductoSerializer(productos_carrito, many=True)
        return Response(serializer.data, status=200)
    except Estado.DoesNotExist:
        return Response({"detail": "Estado 'carrito' no encontrado."}, status=400)

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
