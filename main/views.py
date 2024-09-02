# views

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Usuario, Familia, UsuarioFamilia, Evento, UsuarioEvento
from .forms import UsuarioForm, FamiliaForm, UsuarioFamiliaForm, EventoForm, UsuarioEventoForm, CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import default_storage

# ROL usuario

@login_required
def ver_infopersonal(request):
    try:
        # Obtener el perfil del usuario
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        # Si no existe el perfil, pasar usuario como None para manejar en la plantilla
        usuario = None

    # Si el perfil existe, verificar si hay datos incompletos
    datos_incompletos = False
    if usuario:
        campos_requeridos = [
            usuario.nombres, usuario.apellidos, usuario.n_documento,
            usuario.fecha_nacimiento, usuario.direccion, usuario.telefono,
            usuario.identificacion, usuario.parentesco, usuario.genero,
            usuario.estadoCivil, usuario.escolaridad, usuario.profesion
        ]
        datos_incompletos = any(campo in [None, ''] for campo in campos_requeridos)

    return render(request, 'usuarios/ver.html', {'usuario': usuario, 'datos_incompletos': datos_incompletos})

@login_required
def actualizar_infopersonal(request):
    # Obtener el usuario del modelo Usuario asociado al usuario autenticado
    usuario = get_object_or_404(Usuario, user=request.user)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'usuarios/actualizar.html', {'form': form})

@login_required
def crear_infopersonal(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # No guardar aún en la base de datos
            usuario.user = request.user  # Asignar el usuario actual
            usuario.save()  # Guardar en la base de datos
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear.html', {'form': form})

@login_required
def ver_mifamilia(request):
    try:
        # Obtener el perfil del usuario relacionado con el usuario autenticado
        usuario_actual = request.user.usuario
    except Usuario.DoesNotExist:
        # Si no existe el perfil, pasar como None para manejar en la plantilla
        usuario_actual = None
    
    # Inicializar variables para el contexto
    familia_actual = None
    usuario_familias = []

    if usuario_actual:
        try:
            # Intentar obtener la relación del usuario con su familia
            usuario_familia_actual = UsuarioFamilia.objects.get(usuario=usuario_actual)
            familia_actual = usuario_familia_actual.familia
            usuario_familias = UsuarioFamilia.objects.filter(familia=familia_actual)
        except UsuarioFamilia.DoesNotExist:
            # Si no existe la relación, mantener las variables vacías
            familia_actual = None
            usuario_familias = []

    context = {
        'usuario_familias': usuario_familias,
        'familia_actual': familia_actual,
        'usuario_actual': usuario_actual,  # Opcional, si quieres mostrar información del usuario
    }

    return render(request, 'usuarios/usuarios_familias/listar.html', context)

# ROL admin

# usuarios
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def ver_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/ver.html', {'usuario': usuario})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def listar_usuarios(request):
    usuarios = Usuario.objects.all().select_related('identificacion', 'parentesco', 'genero', 'estadoCivil', 'escolaridad', 'profesion')
    return render(request, 'usuarios/listar.html', {'usuarios': usuarios})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            n_documento = form.cleaned_data['n_documento']
            
            try:
                user = User.objects.get(username=n_documento)
            except User.DoesNotExist:
                user = User.objects.create_user(username=n_documento, password=n_documento)
                group = Group.objects.get(name='Usuario')
                user.groups.add(group)
            
            usuario.user = user
            usuario.save()
            
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def actualizar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/actualizar.html', {'form': form})
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})

# familias

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def listar_familias(request):
    familias = Familia.objects.all()
    return render(request, 'usuarios/familias/listar.html', {'familias': familias})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def crear_familia(request):
    if request.method == 'POST':
        form = FamiliaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_familias')
    else:
        form = FamiliaForm()
    return render(request, 'usuarios/familias/crear.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def actualizar_familia(request, pk):
    familia = get_object_or_404(Familia, pk=pk)
    if request.method == 'POST':
        form = FamiliaForm(request.POST, instance=familia)
        if form.is_valid():
            form.save()
            return redirect('listar_familias')
    else:
        form = FamiliaForm(instance=familia)
    return render(request, 'usuarios/familias/actualizar.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def eliminar_familia(request, pk):
    familia = get_object_or_404(Familia, pk=pk)
    familia.delete()
    return redirect('listar_familias')

# usuario familia 

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def listar_usuario_familia(request):
    usuario_familias = UsuarioFamilia.objects.all()
    return render(request, 'usuarios/usuarios_familias/listar.html', {'usuario_familias': usuario_familias})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def crear_usuario_familia(request):
    if request.method == 'POST':
        form = UsuarioFamiliaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuario_familia')
    else:
        form = UsuarioFamiliaForm()
    return render(request, 'usuarios/usuarios_familias/crear.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def actualizar_usuario_familia(request, pk):
    usuario_familia = get_object_or_404(UsuarioFamilia, pk=pk)
    if request.method == 'POST':
        form = UsuarioFamiliaForm(request.POST, instance=usuario_familia)
        if form.is_valid():
            form.save()
            return redirect('listar_usuario_familia')
    else:
        form = UsuarioFamiliaForm(instance=usuario_familia)
    return render(request, 'usuarios/usuarios_familias/actualizar.html', {'form': form})

def eliminar_usuario_familia(request, pk):
    usuario_familia = get_object_or_404(UsuarioFamilia, pk=pk)
    usuario_familia.delete()
    return redirect('listar_usuario_familia')

# eventos

def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm()
    
    context = {'form': form}
    return render(request, 'eventos/crear.html', context)


def listar_eventos(request):
    eventos = Evento.objects.all()
    context = {'eventos': eventos}
    return render(request, 'eventos/listar.html', context)

def actualizar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento) 
        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm(instance=evento)
    
    context = {'form': form}
    return render(request, 'eventos/actualizar.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    # Eliminar el archivo de la imagen si existe
    if evento.imagen:
        if default_storage.exists(evento.imagen.path):
            default_storage.delete(evento.imagen.path)
    
    evento.delete()
    return redirect('listar_eventos')

# usuarios eventos

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def crear_usuario_evento(request):
    if request.method == 'POST':
        form = UsuarioEventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios_eventos')
    else:
        form = UsuarioEventoForm()
    
    context = {'form': form}
    return render(request, 'eventos/asistencias/crear.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def listar_usuarios_eventos(request):
    usuarios_eventos = UsuarioEvento.objects.all()
    context = {'usuarios_eventos': usuarios_eventos}
    return render(request, 'eventos/asistencias/listar.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def actualizar_usuario_evento(request, pk):
    usuario_evento = get_object_or_404(UsuarioEvento, pk=pk)
    if request.method == 'POST':
        form = UsuarioEventoForm(request.POST, instance=usuario_evento)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios_eventos')
    else:
        form = UsuarioEventoForm(instance=usuario_evento)
    
    context = {'form': form}
    return render(request, 'eventos/asistencias/actualizar.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def eliminar_usuario_evento(request, pk):
    usuario_evento = get_object_or_404(UsuarioEvento, pk=pk)
    if request.method == 'POST':
        usuario_evento.delete()
    return redirect('listar_usuarios_eventos')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def listar_usuarios_por_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    usuarios_eventos = UsuarioEvento.objects.filter(evento=evento)
    context = {
        'evento': evento,
        'usuarios_eventos': usuarios_eventos
    }
    return render(request, 'eventos/asistencias/listar_filtro.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def registrar_usuario_a_evento(request, evento_id=None):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        form = UsuarioEventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = UsuarioEventoForm(initial={'evento': evento})
    
    context = {
        'form': form,
        'evento': evento  
    }
    return render(request, 'eventos/asistencias/crear_filtro.html', context)

# --- login ----

# registrarse

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  
                group = Group.objects.get(name='Usuario') 
                user.groups.add(group)
                login(request, user)  
                return redirect('myData')
            except IntegrityError:
                form.add_error(None, "El nombre de usuario ya existe.")
        else:
            return render(request, 'login/signup.html', {"form": form})

    else:
        form = CustomUserCreationForm()
    return render(request, 'login/signup.html', {"form": form})
        
# iniciar sesion

def signin(request):
    if request.method == 'GET':
        return render(request, 'login/signin.html', {"formAuth": CustomAuthenticationForm()})
    else:
        # Autenticar usuario
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login/signin.html', {"formAuth": CustomAuthenticationForm(), "error": "Usuario o contraseña incorrecta."})
        
        login(request, user)
        
        # Redirigir según grupo
        if user.groups.filter(name='Admin').exists():
            return redirect('listar_usuarios')  # Redirigir a vista de admin
        elif user.groups.filter(name='Usuario').exists():
            return redirect('ver_infopersonal')  # Redirigir a vista de usuario
        else:
            return redirect('index')  # Redirigir si no tiene grupo

# cerrar sesion

@login_required
def signout(request):
    logout(request)
    return redirect('index')

def index(request):
    eventos = Evento.objects.all()
    return render(request, 'bases/landing/index.html', {'eventos': eventos})