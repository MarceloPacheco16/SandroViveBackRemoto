from django.contrib import admin

from app_django.models import Categoria, Producto, Usuario, Cliente, EstadoPedido, Pedido, Pedido_Producto

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(EstadoPedido)
admin.site.register(Pedido)
admin.site.register(Pedido_Producto)
# Register your models here.


