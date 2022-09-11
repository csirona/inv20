from django.contrib import admin

# Register your models here.
from . import models

#se registran los modelos en el admin de django
admin.site.register(models.Producto)
admin.site.register(models.Factura)
admin.site.register(models.Marca)
admin.site.register(models.Categoria)
admin.site.register(models.Proveedor)