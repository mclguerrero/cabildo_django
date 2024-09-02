# forms

from django import forms
from .models import Usuario, TipoIdentificacion, TipoParentesco, TipoGenero, TipoEstadoCivil, TipoEscolaridad, TipoProfesion, Familia, UsuarioFamilia, Evento, UsuarioEvento
from django_select2 import forms as s2forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# usuarios

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombres', 'apellidos', 'n_documento', 'fecha_nacimiento', 'direccion',
            'telefono', 'identificacion', 'parentesco', 'genero', 'estadoCivil', 
            'escolaridad', 'profesion'
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'n_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'identificacion': forms.Select(attrs={'class': 'form-select'}),
            'parentesco': forms.Select(attrs={'class': 'form-select'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'estadoCivil': forms.Select(attrs={'class': 'form-select'}),
            'escolaridad': forms.Select(attrs={'class': 'form-select'}),
            'profesion': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['identificacion'].queryset = TipoIdentificacion.objects.all()
            self.fields['identificacion'].empty_label = "Selecciona tipo de identificación"

            self.fields['parentesco'].queryset = TipoParentesco.objects.all()
            self.fields['parentesco'].empty_label = "Selecciona tipo de parentesco"

            self.fields['genero'].queryset = TipoGenero.objects.all()
            self.fields['genero'].empty_label = "Selecciona género"

            self.fields['estadoCivil'].queryset = TipoEstadoCivil.objects.all()
            self.fields['estadoCivil'].empty_label = "Selecciona estado civil"

            self.fields['escolaridad'].queryset = TipoEscolaridad.objects.all()
            self.fields['escolaridad'].empty_label = "Selecciona nivel de escolaridad"

            self.fields['profesion'].queryset = TipoProfesion.objects.all()
            self.fields['profesion'].empty_label = "Selecciona profesión"

# familia

class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        fields = ['n_familia']

        widgets = {
            'n_familia': forms.TextInput(attrs={'class': 'form-control'}),
        }

# usuario familia

class UserSearch(s2forms.ModelSelect2Widget):
    search_fields = [
        'nombres__icontains',
        'apellidos__icontains',
        'n_documento__icontains',
    ]
    
class FamiliaSearch(s2forms.ModelSelect2Widget):
    search_fields = ['n_familia__icontains',]
        
class UsuarioFamiliaForm(forms.ModelForm):
    class Meta:
        model = UsuarioFamilia
        fields = ['usuario', 'familia']

        widgets = {
            'usuario': UserSearch(attrs={'class': 'form-select'}),
            'familia': FamiliaSearch(attrs={'class': 'form-select'}),
        }
        
# evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'imagen']  # Incluye los nuevos campos

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

# usuario evento UsuarioEvento

class EventoSearch(s2forms.ModelSelect2Widget):
    search_fields = ['nombre__icontains',]

class UsuarioEventoForm(forms.ModelForm):
    class Meta:
        model = UsuarioEvento
        fields = ['usuario', 'evento']

        widgets = {
            'usuario': UserSearch(attrs={'class': 'form-select'}),
            'evento': forms.HiddenInput(),
        }

# login

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita Contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'password']
