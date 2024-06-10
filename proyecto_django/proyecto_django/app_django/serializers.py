from rest_framework import serializers

from django.contrib.auth.hashers import make_password  # Importa make_password

from app_django.models import Categoria, Producto, Usuario, Cliente, Empleado, Estado, Pedido, Pedido_Producto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id','nombre','descripcion','activo')

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id','nombre','descripcion','talle','color','categoria','precio','cantidad','cantidad_disponible','cantidad_limite','imagen','observaciones','activo')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id','email','contrasenia','cant_intentos','activo')
        # extra_kwargs = {'contrasenia': {'write_only': True}} #2

    # 3 
    # SIN CODIGO

    # 2
    # def create(self, validated_data):
    #     validated_data['contrasenia'] = make_password(validated_data['contrasenia'])
    #     return super(UsuarioSerializer, self).create(validated_data)

    # def update(self, instance, validated_data):
    #     if 'contrasenia' in validated_data:
    #         validated_data['contrasenia'] = make_password(validated_data['contrasenia'])
    #     return super(UsuarioSerializer, self).update(instance, validated_data)

    # 1
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['contrasenia'] = '*' * 8  # Cambia la longitud según tus necesidades
    #     return representation
    
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id','nombre','apellido','telefono','domicilio','localidad','provincia','codigo_postal','usuario','activo')

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ('id','nombre','apellido','rol','usuario','activo')

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ('id','tipo_estado')

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('id','cliente','fecha_creacion','fecha_pactada','fecha_entregada','estado','total','observaciones')

class Pedido_ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido_Producto
        fields = ('id','pedido','producto','cantidad','sub_total','total')

