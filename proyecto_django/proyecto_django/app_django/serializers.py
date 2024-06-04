from rest_framework import serializers

from app_django.models import Categoria, Producto, Usuario, Cliente, Estado, Pedido, Pedido_Producto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('nombre','descripcion','activo')

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('nombre','descripcion','talle','color','categoria','precio','cantidad','cantidad_disponible','cantidad_limite','imagen','observaciones','activo')


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('usuario','contrasenia','rol','activo')

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('nombre','apellido','email','telefono','domicilio','localidad','provincia','codigo_postal','usuario','contrasenia','activo')

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ('tipo_estado')

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('cliente','fecha_creacion','fecha_pactada','fecha_entregada','estado','total','observaciones')

class Pedido_ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido_Producto
        fields = ('pedido','producto','cantidad','sub_total','total')

