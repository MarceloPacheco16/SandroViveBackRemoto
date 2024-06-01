from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^categoria$', views.CategoriaList.as_view()),
    re_path(r'^categoria/(?P<pk>[0-9]+)$', views.CategoriaDetail.as_view()),
    re_path(r'^producto$', views.ProductoList.as_view()),
    re_path(r'^producto/(?P<pk>[0-9]+)$', views.ProductoDetail.as_view()),
    re_path(r'^usuario$', views.UsuarioList.as_view()),
    re_path(r'^usuario/(?P<pk>[0-9]+)$', views.UsuarioDetail.as_view()),
    re_path(r'^cliente$', views.ClienteList.as_view()),
    re_path(r'^cliente/(?P<pk>[0-9]+)$', views.ClienteDetail.as_view()),
    re_path(r'^estado$', views.EstadoList.as_view()),
    re_path(r'^estado/(?P<pk>[0-9]+)$', views.EstadoDetail.as_view()),
    re_path(r'^pedido$', views.PedidoList.as_view()),
    re_path(r'^pedido/(?P<pk>[0-9]+)$', views.PedidoDetail.as_view()),
    re_path(r'^pedido_producto$', views.Pedido_ProductoList.as_view()),
    re_path(r'^pedido_producto/(?P<pk>[0-9]+)$', views.Pedido_ProductoDetail.as_view()),
]