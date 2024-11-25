import datetime
from rest_framework import serializers

from django.contrib.auth.hashers import make_password  # Importa make_password

import cloudinary
import cloudinary.uploader

from app_django.models import Categoria, Subcategoria, Producto, Provincia, Localidad, Usuario, Cliente, Empleado, EstadoPedido, Pedido, Pedido_Producto, EstadoPago, MetodoPago
from app_django.models import Factura, Detalle_Envio, Talle

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id','nombre','descripcion','activo')

class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        fields = ('id','nombre','descripcion', 'categoria','activo')

class ProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(allow_null=True, required=False)  # Permitir null y no requerirlo en el POST/PUT
    
    class Meta:
        model = Producto
        fields = ('id','nombre','descripcion','talle','color','categoria', 'subcategoria','precio','cantidad','cantidad_disponible','cantidad_limite','imagen','observaciones','activo')
    
    # def to_representation(self, instance):
    #     # Llamamos al método to_representation original para obtener la representación básica
    #     representation = super().to_representation(instance)
        
    #     # Solo intentamos modificar la URL si existe una imagen
    #     imagen_url = representation.get('imagen')
    #     if imagen_url:
    #         # Verificamos si la URL ya es completa (empieza con 'http')
    #         if not imagen_url.startswith('http'):
    #             # Concatenamos la URL base de Cloudinary si la imagen no tiene una URL completa
    #             representation['imagen'] = f'https://res.cloudinary.com/dophflucq/image/upload/v1/{imagen_url}'
        
    #     return representation
    
    def subir_imagen_a_cloudinary(self, imagen, producto_id):
        now = datetime.datetime.now()
        fecha_actual = now.strftime("%Y%m%d")
        hora_actual = now.strftime("%H%M%S")
        nombre_imagen = f"producto_{producto_id}_{fecha_actual}_{hora_actual}"
        return cloudinary.uploader.upload(imagen, public_id=nombre_imagen, overwrite=True, folder='media')

    def create(self, validated_data):
        # Extraer el campo `imagen` si está presente en los datos validados
        imagen = validated_data.pop('imagen', None)
        producto = Producto.objects.create(**validated_data)

        if imagen:
            upload_result = self.subir_imagen_a_cloudinary(imagen, producto.id)
            producto.imagen = upload_result['secure_url'].split('/')[-1] 
            producto.save()

        return producto

    def update(self, instance, validated_data):
        # Extraer el campo `imagen` si está presente en los datos validados
        imagen = validated_data.pop('imagen', None)
        instance = super().update(instance, validated_data)

        if imagen:
            upload_result = self.subir_imagen_a_cloudinary(imagen, instance.id)
            instance.imagen = upload_result['secure_url'].split('/')[-1]
            instance.save()
        elif 'imagen' in validated_data and validated_data['imagen'] is None:
            # Si `imagen` fue explícitamente enviada como `null`, eliminarla
            instance.imagen = None
            instance.save()

        return instance
    
class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ('id','descripcion')

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ('id','descripcion', 'provincia')

class UsuarioSerializer(serializers.ModelSerializer):
    # write_only=True Solo se usará al escribir datos (POST o PUT), pero no se mostrará cuando se devuelvan los datos (GET)
    # required=False Si el usuario no proporciona una nueva contraseña, no se actualiza.
    # contrasenia = serializers.CharField(write_only=True, required=False)
    contrasenia = serializers.CharField(required=False)

    class Meta:
        model = Usuario
        fields = ('id','email','contrasenia','cant_intentos','activo')

    # Sobreescribir el método update para hashear la nueva contraseña si es proporcionada en PUT o PATCH
    def update(self, instance, validated_data):
        contrasenia = validated_data.pop('contrasenia', None)
        print("contreaseña: ", contrasenia)
        if contrasenia:
            instance.contrasenia = make_password(contrasenia)
        print("contreaseña: ", instance.contrasenia)
        return super().update(instance, validated_data)

    # def update(self, instance, validated_data):
    #     # Si la contraseña está en los datos y es vacía, la eliminamos de validated_data
    #     contrasenia = validated_data.get('contrasenia', None)
        
    #     print("before-contreaseña: ", contrasenia)
    #     if contrasenia == '':
    #         validated_data.pop('contrasenia', None)

    #     print("after-contreaseña: ", contrasenia)
    #     if contrasenia:
    #         instance.contrasenia = make_password(contrasenia)
        
    #     print("final-contreaseña: ", instance.contrasenia)
    #     # Llamamos al método original de actualización
    #     return super().update(instance, validated_data)
     
class ClienteSerializer(serializers.ModelSerializer):
    descuento = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)

    class Meta:
        model = Cliente
        fields = ('id','nombre','apellido','telefono','domicilio','localidad','provincia','codigo_postal','descuento','usuario','activo')

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ('id','nombre','apellido','rol','usuario','activo')

class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPedido
        fields = ('id','estado')

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('id','cliente','fecha_creacion','fecha_pactada','fecha_entregada','estado','total','observaciones')

# class Pedido_ProductoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pedido_Producto
#         fields = ('id','pedido','producto','cantidad','sub_total')
class Pedido_ProductoSerializer(serializers.ModelSerializer):
    producto_id = serializers.IntegerField(source='producto.id', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_precio = serializers.DecimalField(source='producto.precio', max_digits=10, decimal_places=2, read_only=True)
    producto_imagen = serializers.ImageField(source='producto.imagen', read_only=True)
    pedido_id = serializers.IntegerField(source='pedido.id', read_only=True)  # Aquí incluimos el ID del pedido
    
    class Meta:
        model = Pedido_Producto
        fields = ('id', 'pedido_id', 'producto_id', 'producto_nombre', 'producto_precio', 'producto_imagen', 'cantidad', 'sub_total')

class EstadoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPago
        fields = ('id','estado')

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = ('id','metodo')

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ('id','pedido','fecha_emision','descuento','iva','total','estado_pago','metodo_pago', 'observaciones')

class Detalle_EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Envio
        fields = ('id','pedido','domicilio','localidad','provincia', 'fecha_creacion', 'comentario', 'observaciones')

class TalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talle
        fields = ('id','nombre','descripcion','activo')