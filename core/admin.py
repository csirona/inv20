from django.contrib import admin

# Register your models here.
from . import models
#Options

class ProductoAdmin(admin.ModelAdmin):
    list_display= ("codigo", "nombre", "estado")
    search_fields =["nombre"]

#se registran los modelos en el admin de django
admin.site.register(models.Producto, ProductoAdmin)
admin.site.register(models.Factura)
admin.site.register(models.Marca)
admin.site.register(models.Categoria)
admin.site.register(models.Proveedor)