from django.db import models

from django.contrib.auth.hashers import make_password, check_password  # Importa make_password y check_password
# Create your models here.

class Categoria (models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=150)
    activo = models.IntegerField() # 0: Inactivo 1: Activo
    
class Subcategoria (models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)
    activo = models.IntegerField() # 0: Inactivo 1: Activo

class Producto (models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=250)
    talle = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=15)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)
    subcategoria = models.ForeignKey(Subcategoria, null=True, on_delete=models.SET_NULL)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    cantidad_disponible = models.IntegerField()
    cantidad_limite = models.IntegerField()
    imagen = models.ImageField(blank=True)
    observaciones = models.TextField(blank=True, max_length=200)
    activo = models.IntegerField() # 0: Inactivo 1: Activo

class Provincia (models.Model):
    descripcion = models.CharField(max_length=60)

class Localidad (models.Model):
    descripcion = models.CharField(max_length=80)
    provincia = models.ForeignKey(Provincia, null=True, on_delete=models.SET_NULL)

class Usuario (models.Model):
    email = models.EmailField(max_length=30, unique=True)
    contrasenia = models.CharField(max_length=128)
    cant_intentos = models.IntegerField(default=0)
    activo = models.IntegerField(default=1) # 0: Inactivo 1: Activo, 2: Bloqueado

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo encripta la contraseña si es un nuevo objeto
            self.contrasenia = make_password(self.contrasenia)
        super().save(*args, **kwargs)
        
    # def save(self, *args, **kwargs):
    #     if self.pk is None:  # Only hash the password when the user is created
    #         self.contrasenia = make_password(self.contrasenia)
    #     super().save(*args, **kwargs)

    # def check_password(self, password):
    #     return check_password(password, self.contrasenia)
    
    # def save(self, *args, **kwargs):
    #     if not self.pk:  # Si es un objeto nuevo, encripta la contraseña
    #         self.contrasenia = make_password(self.contrasenia)
    #     super().save(*args, **kwargs)

class Cliente (models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    telefono = models.CharField(max_length=15)
    domicilio = models.CharField(max_length=60)
    localidad = models.CharField(max_length=80)
    provincia = models.CharField(max_length=60)
    codigo_postal = models.CharField(max_length=15)
    usuario = models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL)
    activo = models.IntegerField() # 0: Inactivo 1: Activo

class Empleado (models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    rol = models.CharField(max_length=15)
    usuario = models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL)
    activo = models.IntegerField() # 0: Inactivo 1: Activo

class Estado (models.Model):
    tipo_estado = models.CharField(max_length=10)

class Pedido (models.Model):
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)
    fecha_creacion = models.DateField(auto_now=True)
    fecha_pactada = models.DateField(null=True, blank=True)  # Permitir null y que sea opcional
    fecha_entregada = models.DateField(null=True, blank=True)  # Permitir null y que sea opcional
    estado = models.ForeignKey(Estado, null=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, max_length=200)

class Pedido_Producto(models.Model):
    pedido = models.ForeignKey(Pedido, null=True, on_delete=models.SET_NULL)
    producto = models.ForeignKey(Producto, null=True, on_delete=models.SET_NULL)
    cantidad = models.IntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    # total = models.DecimalField(max_digits=10, decimal_places=2)

class Factura(models.Model):

    pedido = models.ForeignKey(Pedido, null=True, on_delete=models.SET_NULL)
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=20, default='Pendiente')  # Posibles valores: Pendiente, Pagado, Cancelado
    metodo_pago = models.CharField(max_length=50)  # Ejemplos: MercadoPago, Efectivo
    observaciones = models.TextField(blank=True, max_length=200)  # Notas adicionales sobre la factura

class Detalle_Envio(models.Model):
    pedido = models.ForeignKey(Pedido, null=True, on_delete=models.SET_NULL)
    domicilio = models.CharField(max_length=60)
    localidad = models.CharField(max_length=80)
    provincia = models.CharField(max_length=60)
    fecha_creacion = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, max_length=200)  # Notas adicionales sobre el Detalle de Envio