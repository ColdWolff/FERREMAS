from django.urls import path
from . import views
urlpatterns = [
    # Usar una cadena vacía para que sea la URL de inicio.
    path("", views.index, name="index"),
    path("hnf", views.hnf, name="hnf"),
    path("carrito", views.c, name="c"),
    path("converter", views.converter, name="converter"),
    path('convertir-usd-a-clp/', views.convertir_usd_a_clp, name='convertir_usd_a_clp'),
]
