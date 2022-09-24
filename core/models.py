from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=150, default='Generico')

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=150, default='Generico')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=100,primary_key=True)
    descripcion = models.TextField(default="descripcion")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE,null=True,blank=True)
    precio = models.PositiveIntegerField(null=True,blank=True)
    imagen = models.ImageField(upload_to='core/images/',null=True,blank=True)
    estado = models.BooleanField(default=False)
    fecha_baja = models.DateTimeField(null=True, blank=True)
    almacen = models.CharField(max_length=150,null=True,blank=True)
    serie = models.CharField(max_length=20,null=True,blank=True)
    #qr

    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'

    def formatNumber(self):
        espanol=True
        if type(self.precio) != int and type(self.precio) != float:
            return self.precio
        d={'.':',', ',':'.'}
        return ''.join(d.get(s, s) for s in f"{self.precio:,.{0}f}") \
            if espanol \
            else f"{self.precio:,.{0}f}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name



class Proveedor(models.Model):
    #Proveedor
    rut_p = models.CharField(max_length=20)
    nombre_p = models.CharField(max_length=50)
    direccion= models.CharField(max_length=50)
    cuidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_p

class Factura(models.Model):
    descripcion = models.TextField(max_length=50, null=True)
    codigo = models.PositiveIntegerField()
    related_productos = models.ManyToManyField(Producto,blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_compra = models.DateTimeField(null=True,blank=True,default=timezone.now)
    neto = models.PositiveIntegerField(null=True,blank=True)
    estado = models.BooleanField(default=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    autor = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return str(self.id)


# class ProductoFactura(models.Model):
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = [['producto','factura']]

#     def __str__(self):
#         return f'{self.producto} en {self.factura}'
