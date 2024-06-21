from django.urls import path, re_path
from . import views
from .views import get_public_key
# from .views import login

urlpatterns = [
    re_path(r'^categoria$', views.CategoriaList.as_view()),
    re_path(r'^categoria/(?P<pk>[0-9]+)$', views.CategoriaDetail.as_view()),
    re_path(r'^producto$', views.ProductoList.as_view()),
    re_path(r'^producto/(?P<pk>[0-9]+)$', views.ProductoDetail.as_view()),
    re_path(r'^provincia$', views.ProvinciaList.as_view()),
    re_path(r'^provincia/(?P<pk>[0-9]+)$', views.ProvinciaDetail.as_view()),    
    re_path(r'^localidad$', views.LocalidadList.as_view()),
    re_path(r'^localidad/(?P<pk>[0-9]+)$', views.LocalidadDetail.as_view()),
    re_path(r'^usuario$', views.UsuarioList.as_view()),
    re_path(r'^usuario/(?P<pk>[0-9]+)$', views.UsuarioDetail.as_view()),
    re_path(r'^cliente$', views.ClienteList.as_view()),
    re_path(r'^cliente/(?P<pk>[0-9]+)$', views.ClienteDetail.as_view()),
    re_path(r'^empleado$', views.EmpleadoList.as_view()),
    re_path(r'^empleado/(?P<pk>[0-9]+)$', views.EmpleadoDetail.as_view()),
    re_path(r'^estado$', views.EstadoList.as_view()),
    re_path(r'^estado/(?P<pk>[0-9]+)$', views.EstadoDetail.as_view()),
    re_path(r'^pedido$', views.PedidoList.as_view()),
    re_path(r'^pedido/(?P<pk>[0-9]+)$', views.PedidoDetail.as_view()),
    re_path(r'^pedido_producto$', views.Pedido_ProductoList.as_view()),
    re_path(r'^pedido_producto/(?P<pk>[0-9]+)$', views.Pedido_ProductoDetail.as_view()),
    re_path(r'^factura$', views.FacturaList.as_view()),
    re_path(r'^factura/(?P<pk>[0-9]+)$', views.FacturaDetail.as_view()),
    re_path(r'^detalle_envio$', views.Detalle_EnvioList.as_view()),
    re_path(r'^detalle_envio/(?P<pk>[0-9]+)$', views.Detalle_EnvioDetail.as_view()),
    path('get-public-key/', get_public_key),
    # path('login/', login),
    path('verificar-credenciales/', views.verificar_credenciales),
    path('localidad/provincia/<int:provincia_id>/', views.localidades_por_provincia),
]