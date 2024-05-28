from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Inicio
    path("", views.index, name="index"),
    # Login & Sign-up
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    

    path("carrito", views.carrito, name="carrito"),
    path("convertir", views.convertir_divisa, name="convertir"),
    path("reconvertir", views.reconvertir_divisa, name="reconvertir"),

    # PRODUCTO
    path("create_prod", views.productoAdd, name="create_prod"),
    path('read_prod/<str:pk>', views.productoRead, name='read_prod'),
    path('update_prod', views.productoUpdate, name='update_prod'),
    path('delete_prod/<str:pk>', views.productoDel, name='delete_prod'),
    path('list_prod', views.productoList, name='list_prod'),

    # STOCK
    path("create_stock", views.stockAdd, name="create_stock"),
    path('read_stock/<str:pk>', views.stockRead, name='read_stock'),
    path('update_stock', views.stockUpdate, name='update_stock'),
    path('delete_stock/<str:pk>', views.stockDel, name='delete_stock'),
    path('list_stock', views.stockList, name='list_stock'),

    # TRANSBANK
    path('compra/iniciar/', views.iniciar_compra, name='iniciar_compra'),
    path('compra/completada/', views.compra_completada, name='compra_completada'),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

