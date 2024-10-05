from rest_framework import serializers

from django.contrib.auth.hashers import make_password  # Importa make_password

from app_django.models import Categoria, Subcategoria, Producto, Provincia, Localidad, Usuario, Cliente, Empleado, Estado, Pedido, Pedido_Producto, Factura, Detalle_Envio, Talle

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id','nombre','descripcion','activo')

class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        fields = ('id','nombre','descripcion', 'categoria','activo')

class ProductoSerializer(serializers.ModelSerializer):
    # subcategoria = serializers.PrimaryKeyRelatedField(queryset=Subcategoria.objects.all(), allow_null=True)
    # imagen = serializers.ImageField(allow_null=True, required=False)  # Permitir null y no requerirlo en el POST/PUT
    imagen = serializers.ImageField(allow_null=True, required=False)  # Permitir null y no requerirlo en el POST/PUT
    
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

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ('id','pedido','fecha_emision','total','estado_pago','metodo_pago', 'observaciones')

class Detalle_EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Envio
        fields = ('id','pedido','domicilio','localidad','provincia', 'fecha_creacion', 'observaciones')


class TalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talle
        fields = ('id','nombre','descripcion','activo')