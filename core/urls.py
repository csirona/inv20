from django.urls import path
#se importa todo de views
from . import views
from django.conf import settings
from django.conf.urls.static import static


#se asigna ruta, se toma funcion de views y se le da nombre
urlpatterns = [
    path('',views.Index,name='index'),

    path('tienda', views.Tienda, name="Tienda"),
    path('confirm/',views.Confirm,name='confirm'),
    path('facturaactiva/',views.Kitchen,name='kitchen'),
    path('facturas/',views.KitchenAll,name='kitchenAll'),


    # #formularios
    # #path('registros/',views.registros,name='registros'),


    path('ready/<int:comd_id>',views.Ready,name='ready'),

    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    # path("password_change", views.password_change, name="password_change"),
    # path("password_reset", views.password_reset_request, name="password_reset"),
    # path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),

    path('listafactura/', views.ListaFacturas, name='listfactura'),

    path('listaproducto/', views.ListaProducto, name='listproduct'),
    path('listaproveedor/', views.ListaProveedor, name='listproveedor'),
    path('listamarca/', views.ListaMarca, name='listmarca'),
    path('listacategoria/', views.ListaCategoria, name='listcategoria'),

    path('nuevoproducto/', views.NuevoProducto, name='newproduct'),
    path('nuevafactura/', views.nuevaFactura, name='newfactura'),
    path('nuevamarca/', views.NuevaMarca, name='newmarca'),
    path('nuevacategoria/', views.NuevaCategoria, name='newcategoria'),
    path('nuevoproveedor/', views.NuevoProveedor, name='newproveedor'),

    path('detallefactura/<int:id_f>/', views.detalleFactura, name='detallefactura'),
    path('detalleproducto/<str:id_p>/', views.detalleProducto, name='detalleproducto'),

    path('modificarproducto/<str:id>', views.Update, name='updateproduct'),
    path('modificarproveedor/<str:id>', views.UpdateProveedor, name='updateproveedor'),
    path('modificarmarca/<str:id>', views.UpdateMarca, name='updatemarca'),
    path('modificarcategoria/<str:id>', views.UpdateCategoria, name='updatecategoria'),

    path('confirmcambioestado/<str:cod>', views.confirmCambioEstado, name='confirmcambioestado'),

    path('almacen/',views.Almacen,name='almacen'),

    path('setalmacen/<str:cod>',views.setAlmacen,name='setalmacen'),
    path('setserie/<str:cod>',views.setSerie,name='setserie'),

    path('qrcode/<str:qr>',views.generate_qrcode,name='qrcode'),
    path('cambiarestado/<str:prod>',views.cambiarEstado,name='cambiarEstado'),

    path('eliminarfactura/<str:cod>',views.DeleteFactura,name='deletefactura'),
    path('eliminar/<str:cod>',views.DeleteConfirmFactura,name='delete'),

    path('export/xls', views.export_users_xls, name='export_users_xls'),
    path('exportstock/xls/>', views.export_stock_xls, name='export_stock_xls'),

    path('stock/',views.CountStock,name='stock'),

    path('buscarstock/',views.StockBuscar,name='buscarstock'),
    # path('generatepdf/',views.generate_pdf,name='generatepdf'),
    # path('htmltopdf/',views.htmlToPdf,name='htmltopdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'core.views.error_404_view'

