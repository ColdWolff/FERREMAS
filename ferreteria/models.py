from django.db import models
from django.contrib.auth.models import User

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nom_prov = models.CharField(max_length=10)

class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    nom_cargo = models.CharField(max_length=10)

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    desc_cat = models.CharField(max_length=100)

class Cliente(models.Model):
    rut_cli = models.CharField(primary_key=True, max_length=10)
    nombre_cli = models.CharField(max_length=100)
    email_cli = models.EmailField(max_length=100)

class Empleado(models.Model):
    rut_emp = models.CharField(primary_key=True, max_length=10)
    nombre_emp = models.CharField(max_length=100)
    email_emp = models.EmailField(max_length=100)
    telefono_emp = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=15)
    id_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=10)
    codigo_prod = models.CharField(max_length=10)
    nombre_prod = models.CharField(max_length=100)
    desc_prod = models.CharField(max_length=300)
    precio_prod = models.FloatField()
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Stock(models.Model):
    id_stock = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.cantidad * self.producto.precio_prod