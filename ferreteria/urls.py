from django.urls import path
from . import views
urlpatterns = [
    # Usar una cadena vacía para que sea la URL de inicio.
    path("", views.index, name="index"),
    path("hnf", views.hnf, name="hnf"),
    path("carrito", views.carrito, name="carrito"),
    path("convertir", views.convertir_divisa, name="convertir"),
    path("reconvertir", views.reconvertir_divisa, name="reconvertir"),
]
