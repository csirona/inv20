from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


#se define clase forms
#se asigna tipo de objeto y declarar parametros del formulario


class DateInput(forms.DateInput):
    input_type = 'date'


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['categoria','marca','nombre','observacion','precio','imagen','cantidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'observacion': forms.TextInput(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class':'form-select'}),
            'marca': forms.Select(attrs={'class':'form-select'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
        }

class SerieProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['serie']
        widgets = {
            'serie': forms.TextInput(attrs={'class':'form-control'}),
        }

class ProductoFormUpdate(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre','observacion','serie','categoria','marca','precio','imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'observacion': forms.TextInput(attrs={'class':'form-control'}),
            'serie': forms.TextInput(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class':'form-select'}),
            'marca': forms.Select(attrs={'class':'form-select'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
        }

class AlmacenForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['almacen']
        widgets = {
            'almacen': forms.TextInput(attrs={'class':'form-control'}),

        }


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }

class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['codigo','descripcion','fecha_compra','proveedor', 'financiado']
        widgets = {
                    'fecha_compra': DateInput(),
                    'descripcion': forms.TextInput(attrs={'class':'form-control'}),

                }
        labels = {
            'codigo': 'Nº Factura',
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['rut_p','nombre_p','direccion','cuidad']
        labels = {
            'rut_p': 'Rut.',
            'nombre_p': 'Nombre.',
            'direccion': 'Direccion',
            'cuidad': 'Cuidad',


        }


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user