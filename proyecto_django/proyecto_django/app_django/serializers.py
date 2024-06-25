from rest_framework import serializers

from django.contrib.auth.hashers import make_password  # Importa make_password

from app_django.models import Categoria, Subcategoria, Producto, Provincia, Localidad, Usuario, Cliente, Empleado, Estado, Pedido, Pedido_Producto, Factura, Detalle_Envio

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id','nombre','descripcion','activo')

class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        fields = ('id','nombre','descripcion', 'categoria','activo')

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id','nombre','descripcion','talle','color','categoria', 'subcategoria','precio','cantidad','cantidad_disponible','cantidad_limite','imagen','observaciones','activo')

class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ('id','descripcion')

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ('id','descripcion', 'provincia')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id','email','contrasenia','cant_intentos','activo')
    
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

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ('id','pedido','fecha_emision','total','estado_pago','metodo_pago', 'observaciones')

class Detalle_EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Envio
        fields = ('id','pedido','domicilio','localidad','provincia', 'fecha_creacion', 'observaciones')

