from django.shortcuts import render
import xlwt
from datetime import datetime
import io
import os
from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from io import BytesIO
from core.forms import CategoriaForm, MarcaForm
from core.models import Categoria, Factura, Marca, Producto, Proveedor
import qrcode
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


from .models import *
from .forms import *
from django.shortcuts import (get_object_or_404,
							render,
							HttpResponseRedirect)
from django.db.models import Q
from django.contrib import messages

from django.http import FileResponse

def Index(request):
    return render(request,'core/index.html')

def Tienda(request):
    #Se obtiene todos los objetos de cada tipp=o
    productos = Producto.objects.filter(estado=True)

    if request.method == 'POST':
        form = FacturaForm(request.POST)

        if form.is_valid() :
            f=form.save(commit=False)
            f.save()

        return redirect('confirm')
    else:
        form = FacturaForm()
    #se asigna a una variable lo obtenido del buscador
    queryset= request.GET.get("buscar")
    #si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        productos = Product.objects.filter(
            Q(id__icontains = queryset)
        ).distinct()


    #Contezto de datos
    context={
        'productos':productos,
        'form':form,

    }
    #Se retorna un render del template correspondiente a la ruta y le pasa el contexto
    return render(request, "core/tienda.html",context)

@login_required
def NuevaMarca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)

        if form.is_valid() :
            f=form.save(commit=False)
            f.save()

        return redirect('/')
    else:
        form = MarcaForm()
    #Contezto de datos
    context={
        'form':form,
    }
    return render(request, "core/newmarca.html",context)
@login_required
def NuevaCategoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)

        if form.is_valid() :
            f=form.save(commit=False)
            f.save()

        return redirect('/')
    else:
        form = CategoriaForm()
    #Contezto de datos
    context={
        'form':form,
    }
    return render(request, "core/newcategoria.html",context)
@login_required
def NuevoProveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)

        if form.is_valid() :
            f=form.save(commit=False)
            f.save()

        return redirect('listproveedor')
    else:
        form = ProveedorForm()
    context={
        'form':form,
    }
    return render(request, "core/newproveedor.html",context)
@login_required
def nuevaFactura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)

        if form.is_valid() :
            f=form.save(commit=False)
            username = None
            if request.user.is_authenticated:
                username = request.user.username
                f.autor=  username
            f.save()

        return redirect('kitchen')
    else:
        form = FacturaForm()
    #Contezto de datos
    context={
        'form':form,
    }
    #Se retorna un render del template correspondiente a la ruta y le pasa el contexto
    return render(request, "core/newfactura.html",context)


@login_required
def NuevoProducto(request):
    p=Producto.objects.all()
    le=len(p)
    f=Factura.objects.last()
    facturas=Factura.objects.all()
    form=ProductoForm(request.POST, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            a=form.save(commit=False)
            i=0
            c=a.cantidad
            for i in range(c):
                a.codigo= a.nombre[0:3] + str(le+i)
                a.estado=True
                a.save()
                f.related_productos.add(a)
                print(i)
                print(a.codigo)
            return HttpResponseRedirect("/facturaactiva/")
        else:
            print('error')
    context={
            "product":p,
            "form":form,
            "facturas":facturas,
            }
    return render(request, 'core/new_product.html',context)

@login_required
def Confirm(request):
    p = Producto.objects.filter(estado=True)
    context={
        'productos':p,
    }
    return render(request, 'core/confirm.html',context)


@login_required
def Kitchen(request):
    fact= None
    prods=None
    #Filtrar facturas por autor
    cmd = Factura.objects.filter(autor=request.user.username)
    #Recorrer facturas y cuando estado == True, la guarda y a sus productos
    for f in cmd:
        if f.estado:
            #fact es la factura activa
            fact=f
            prods = f.related_productos.all()

    context={
        "factura":fact,
        "prods":prods
    }
    return render(request, 'core/facturaActiva.html',context)

@login_required
def KitchenAll(request):
    cmd = Factura.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(cmd, 6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context={
        "cmd":users,
    }
    return render(request, 'core/kitchenall.html',context)

@login_required
def Ready(request,comd_id):
    cmd1 = Factura.objects.filter(autor=request.user.username)
    cmd=cmd1.get(id=comd_id)
    cmd.estado=False
    cmd.save()
    return redirect('/listafactura')

@login_required
def ListaProveedor(request):
    prov=Proveedor.objects.all()
    #se asigna a una variable lo obtenido del buscador
    queryset= request.GET.get("buscar")
    #si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        prov = Proveedor.objects.filter(
            Q(nombre_p__icontains = queryset)| Q(rut_p__icontains=queryset)
        ).distinct()
    context={
        "product":prov,
    }
    return render(request, 'core/list_proveedor.html',context)

@login_required
def ListaMarca(request):
    prov=Marca.objects.all()
    #se asigna a una variable lo obtenido del buscador
    queryset= request.GET.get("buscar")
    #si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        prov = Marca.objects.filter(
            Q(nombre__icontains = queryset)
        ).distinct()
    context={
        "product":prov,
    }
    return render(request, 'core/list_marca.html',context)
@login_required
def ListaCategoria(request):
    prov=Categoria.objects.all()
    #se asigna a una variable lo obtenido del buscador
    queryset= request.GET.get("buscar")
    #si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        prov = Categoria.objects.filter(
            Q(nombre__icontains = queryset)
        ).distinct()
    context={
        "product":prov,
    }
    return render(request, 'core/list_categoria.html',context)

#Listar productos
@login_required
def ListaProducto(request):
    productos=Producto.objects.all()
    #se asigna a una variable lo obtenido del buscador
    queryset= request.GET.get("buscar")
    #si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        productos = Producto.objects.filter(
            Q(nombre__icontains = queryset)| Q(codigo__icontains=queryset)
        ).distinct()
    context={
        "product":productos,
    }
    return render(request, 'core/list_producto.html',context)

@login_required
def ListaFacturas(request):
    facturas=Factura.objects.all()
    queryset= request.GET.get("buscar")
    #si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        facturas = Factura.objects.filter(
             Q(codigo__icontains=queryset)
            | Q(fecha_compra__icontains=queryset)

        ).distinct()
    context={
        "facturas":facturas,
    }
    return render(request, 'core/list_factura.html',context)

@login_required
def detalleFactura(request,id_f):
    factura=Factura.objects.get(id=id_f)

    context={
        "factura":factura,
    }
    return render(request, 'core/detalle_factura.html',context)

@login_required
def detalleProducto(request,id_p):
    producto=Producto.objects.get(codigo=id_p)
    context={
        "producto":producto,
    }
    return render(request, 'core/detalle_producto.html',context)



@login_required
@login_required
def Update(request,id):
    context={

    }
    obj = Producto.objects.get( codigo = id)
    username = request.user.username

    form = ProductoFormUpdate(request.POST or None,request.FILES or None, instance = obj)
    if form.is_valid():
        img_path = obj.imagen.path
        if os.path.exists(img_path):
            os.remove(img_path)

        p=form.save()
        p.last_mod_user = username
        p.last_mod_time = datetime.now()
        p.save()
        return HttpResponseRedirect("/listaproducto/")
    else:
        print('error')
    context["form"] = form

    return render(request, 'core/update_product.html',context)


@login_required
def UpdateProveedor(request,id):
    context={

    }
    obj = get_object_or_404(Proveedor, id = id)

    form = ProveedorForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/listaproveedor/")
    else:
        print('error')

    context["form"] = form

    return render(request, 'core/update_proveedor.html',context)



@login_required
def UpdateCategoria(request,id):
    context={

    }
    obj = get_object_or_404(Categoria, id = id)

    form = CategoriaForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/listacategoria/")
    else:
        print('error')

    context["form"] = form

    return render(request, 'core/update_categoria.html',context)


@login_required
def UpdateMarca(request,id):
    context={

    }
    obj = get_object_or_404(Marca, id = id)

    form = MarcaForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/listamarca/")
    else:
        print('error')

    context["form"] = form

    return render(request, 'core/update_marca.html',context)

#Registro
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="core/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="core/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("/")

@login_required
def generate_qrcode(request,qr):
    det = 'https://csirona.pythonanywhere.com/detalleproducto/'
    data = det+qr
    img = qrcode.make(data)

    buf = BytesIO()		# BytesIO se da cuenta de leer y escribir bytes en la memoria
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")

    return response

# def generate_pdf(request):
#     #get factura
#     f=Factura.objects.get(id=2)
#     ff=f.related_productos.all()
#     #create bytestream buffer
#     buff= io.BytesIO()

#     #create a canvas
#     c= canvas.Canvas(buff,pagesize=A4,bottomup=0)

#     #create a text object
#     textob= c.beginText()
#     textob.setTextOrigin(inch,inch)
#     textob.setFont("Helvetica",14)

#     #add some line of text
#     lines = [
#         "This is line 1",
#         "This is line 2",
#         "This is line 3"
#     ]

#     cadena='cadenaaaa'
#     x=0
#     y=0
#     #loop
#     textob.textLine('factura: '+str(f.codigo))
#     textob.textLine('fecha: '+str(f.fecha_compra))
#     textob.textLine('descripcion: '+str(f.descripcion))
#     for p in ff:
#         textob.textLine('Nombre: '+p.nombre)
#         textob.textLine()
#         textob.textLine('Codigo: '+p.codigo)
#         textob.textLine()
#         x=10
#         y=y+10
#         archivo_imagen='http://127.0.0.1:8000/detalleproducto/'+ p.codigo
#         #c.drawImage('static/'+p.imagen.url,0, 0)


#         #textob.textLine(qrcode.make('http://127.0.0.1:8000/detalleproducto/'+ p.codigo))

#     #finish up
#     c.drawText(textob)
#     c.showPage()
#     c.save()
#     buff.seek(0)

#     #return smthg
#     return FileResponse(buff, as_attachment=True,filename='generate.pdf')

@login_required
def cambiarEstado(request,prod):
    p=Producto.objects.get(codigo=prod)
    p.estado=False
    p.fecha_baja=datetime.now()
    username = request.user.username
    p.last_cs_user = username
    p.last_cs_time = datetime.now()
    messages.add_message(request, messages.SUCCESS, 'Producto dado de baja')
    p.save()

    print(p.estado)
    return redirect("listproduct")


@login_required
def confirmCambioEstado(request,cod):
    producto=Producto.objects.get(codigo=cod)
    context={
        'product':producto,

    }
    return render(request,'core/cambio_estado_producto.html',context)

def StockBuscar(request):
    s=0
    prod=Producto.objects.all()
    queryset= request.GET.get("buscar")
    #si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        p = Producto.objects.filter(
            Q(nombre__icontains = queryset) |Q(codigo__icontains = queryset)
        ).distinct()
        prod=p.last()
        s=p.count()


    context={
        "queryset":s,
        "prod":prod,
    }
    return render(request, 'core/stockbuscar.html',context)



@login_required
def Almacen(request):
    productos=Producto.objects.all()
    #se asigna a una variable lo obtenido del buscador
    queryset= request.GET.get("buscar")
    #si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        productos = Producto.objects.filter(
            Q(nombre__icontains = queryset)| Q(codigo__icontains=queryset)
            | Q(almacen__icontains=queryset)
        ).distinct()
    context={
        "product":productos,
    }
    return render(request, 'core/almacen.html',context)

@login_required
def setAlmacen(request,cod):
    context={
    }
    obj = get_object_or_404(Producto, codigo = cod)
    form = AlmacenForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/almacen/")
    else:
        print('error')
    context["form"] = form
    return render(request, 'core/setalmacen.html',context)

@login_required
def setSerie(request,cod):
    context={
    }
    obj = get_object_or_404(Producto, codigo = cod)
    form = SerieProductoForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/facturaactiva/")
    else:
        print('error')
    context["form"] = form
    return render(request, 'core/setSerie.html',context)


@login_required
def DeleteFactura(request,cod):
    prods=None
    #Traer la factura por id
    factura = Factura.objects.get(id=cod)
    #Recorrer facturas y cuando estado == True, la guarda y a sus productos
    prods = factura.related_productos.all()
    print(factura)
    print(prods)

    context={
        "factura":factura,
        "prods":prods
    }
    return render(request, 'core/deleteFactura.html',context)


@login_required
def DeleteConfirmFactura(request,cod):
    #Traer la factura por id
    factura = Factura.objects.get(id=cod)
    #Recorrer facturas y cuando estado == True, la guarda y a sus productos
    prods = factura.related_productos.all()
    for p in prods:
        p.delete()

    factura.delete()

    return HttpResponseRedirect("/listafactura/")


#To  excel data

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="productos.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Producto')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Codigo', 'Nombre','Serie', 'Observacion', 'Proveedor','Categoria','Marca','Precio','Estado','Almacen','Factura', 'Fecha de Compra' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Producto.objects.all().values_list('codigo', 'nombre', 'serie', 'observacion','factura__proveedor__nombre_p','categoria__nombre','marca__nombre','precio','estado','almacen','factura__codigo','factura__fecha_compra')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def error_404_view(request, exception):

    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')