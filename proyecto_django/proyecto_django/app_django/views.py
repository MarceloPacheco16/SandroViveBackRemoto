from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import check_password

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

# from django.contrib.auth.hashers import check_password


from app_django.models import Categoria, Producto, Usuario, Cliente, Empleado, Estado, Pedido, Pedido_Producto

from app_django.serializers import CategoriaSerializer, ProductoSerializer, UsuarioSerializer, ClienteSerializer, EmpleadoSerializer, EstadoSerializer, PedidoSerializer, Pedido_ProductoSerializer
# Create your views here.

# # View for login
# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         contrasenia = request.data.get('contrasenia')
        
#         try:
#             usuario = Usuario.objects.get(email=email)
#             if check_password(contrasenia, usuario.contrasenia):
#                 return Response({"message": "Login successful", "usuario_id": usuario.id}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         except Usuario.DoesNotExist:
#             return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# Other views...
class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
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

# class AuthenticateUser(APIView):
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('contrasenia')
        
#         try:
#             usuario = Usuario.objects.get(email=email)
#         except Usuario.DoesNotExist:
#             return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
        
#         if usuario.check_password(password):
#             serializer = UsuarioSerializer(usuario)
#             return Response(serializer.data)
#         else:
#             return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

# def verificar_credenciales(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         contrasenia = request.POST.get('contrasenia')
        
#         try:
#             usuario = Usuario.objects.get(email=email)
#             if check_password(contrasenia, usuario.contrasenia):
#                 usuario_data = {
#                     'id': usuario.id,
#                     'email': usuario.email,
#                     # Agrega otros campos de Usuario si es necesario
#                 }
#                 return JsonResponse(usuario_data)
#             else:
#                 return JsonResponse({})
#         except Usuario.DoesNotExist:
#             return JsonResponse({})
#     else:
#         return JsonResponse({})


# def verificar_credenciales(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         contrasenia = request.POST.get('contrasenia')

#         try:
#             usuario = Usuario.objects.get(email=email)
#             if check_password(contrasenia, usuario.contrasenia):
#                 usuario_data = {
#                     'id': usuario.id,
#                     'email': usuario.email,
#                     # Agrega otros campos de Usuario si es necesario
#                 }
#                 return JsonResponse(usuario_data)
#             else:
#                 return JsonResponse({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         except Usuario.DoesNotExist:
#             return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#     else:
#         return JsonResponse({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @csrf_exempt
# def verificar_credenciales(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         contrasenia = request.POST.get('contrasenia')

#         try:
#             usuario = Usuario.objects.get(email=email)
#             if check_password(contrasenia, usuario.contrasenia):
#                 usuario_data = {
#                     'id': usuario.id,
#                     'email': usuario.email,
#                     # Agrega otros campos de Usuario si es necesario
#                 }
#                 return JsonResponse(usuario_data)
#             else:
#                 return JsonResponse({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         except Usuario.DoesNotExist:
#             return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# @csrf_exempt
# def verificar_credenciales(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         contrasenia = request.POST.get('contrasenia')

#         try:
#             usuario = Usuario.objects.get(email=email)
#             if check_password(contrasenia, usuario.contrasenia):
#                 usuario_data = {
#                     'id': usuario.id,
#                     'email': usuario.email,
#                     # Agrega otros campos de Usuario si es necesario
#                 }
#                 return JsonResponse(usuario_data)
#             else:
#                 return JsonResponse({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         except Usuario.DoesNotExist:
#             return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#     elif request.method == 'GET':
#         return HttpResponse("Método no permitido", status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     else:
#         return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# def verificar_credenciales(request):
#     if request.method == 'GET':
#         email = request.GET.get('email')
#         contrasenia = request.GET.get('contrasenia')

#         try:
#             usuario = Usuario.objects.get(email=email)
#             if check_password(contrasenia, usuario.contrasenia):
#                 usuario_data = {
#                     'id': usuario.id,
#                     'email': usuario.email,
#                     # Agrega otros campos de Usuario si es necesario
#                 }
#                 return JsonResponse(usuario_data)
#             else:
#                 return JsonResponse({"detail": "Invalid credentials"}, status=401)
#         except Usuario.DoesNotExist:
#             return JsonResponse({"detail": "User not found"}, status=404)
#     else:
#         return JsonResponse({"detail": "Method not allowed"}, status=405)

@csrf_exempt
def verificar_credenciales(request):
    # Verificar que el método de la solicitud sea GET
    if request.method == 'GET':
        # Obtener parámetros 'email' y 'contrasenia' de la solicitud GET
        email = request.GET.get('email')
        contrasenia = request.GET.get('contrasenia')

        try:
            # Intentar obtener el usuario con el email proporcionado
            usuario = Usuario.objects.get(email=email)
            
            # Verificar si el usuario está bloqueado
            if usuario.activo == 2:
                return JsonResponse({"detalle": "El usuario está bloqueado"}, status=403)

            # Verificar si la contraseña es correcta
            if check_password(contrasenia, usuario.contrasenia):
                # Preparar los datos del usuario para la respuesta
                usuario_data = {
                    'id': usuario.id,
                    'email': usuario.email,
                    'activo': usuario.activo,
                    # Agregar otros campos de Usuario si es necesario
                }
                # Resetear el conteo de intentos fallidos
                usuario.cant_intentos = 0
                # Guardar los cambios en la base de datos
                usuario.save()
                # Devolver los datos del usuario en una respuesta JSON
                return JsonResponse(usuario_data)
            else:
                # Incrementar el conteo de intentos fallidos
                usuario.cant_intentos += 1
                # Verificar si los intentos fallidos son menores a 3
                if usuario.cant_intentos < 3:
                    # Guardar los cambios en la base de datos
                    usuario.save()
                    # Devolver una respuesta indicando credenciales inválidas
                    return JsonResponse({"detalle": "Email o Contraseña incorrectos"}, status=401)
                # Si los intentos fallidos son 3 o más, bloquear al usuario
                if usuario.cant_intentos >= 3:
                    usuario.activo = 2  # Bloquear usuario
                    # Guardar los cambios en la base de datos
                    usuario.save()
                    # Devolver una respuesta indicando que el usuario está bloqueado
                    return JsonResponse({"detalle": "Credenciales inválidas, usuario bloqueado"}, status=403)
        except Usuario.DoesNotExist:
            # Devolver una respuesta indicando que el usuario no fue encontrado
            return JsonResponse({"detalle": "Usuario no encontrado"}, status=404)
    else:
        # Devolver una respuesta indicando que el método no está permitido
        return JsonResponse({"detalle": "Método no permitido"}, status=405)
