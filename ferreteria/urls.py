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
]
