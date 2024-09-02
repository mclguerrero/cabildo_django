# models

from django.db import models
from django.contrib.auth.models import User

# usuario

class TipoIdentificacion(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre}"


class TipoParentesco(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre}"


class TipoGenero(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre}"


class TipoEstadoCivil(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre}"


class TipoEscolaridad(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre}"


class TipoProfesion(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre}"


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    n_documento = models.CharField(max_length=45)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.CASCADE)
    parentesco = models.ForeignKey(TipoParentesco, on_delete=models.CASCADE)
    genero = models.ForeignKey(TipoGenero, on_delete=models.CASCADE)
    estadoCivil = models.ForeignKey(TipoEstadoCivil, on_delete=models.CASCADE)
    escolaridad = models.ForeignKey(TipoEscolaridad, on_delete=models.CASCADE)
    profesion = models.ForeignKey(TipoProfesion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    def familias(self):
        return self.usuariofamilia_set.all()

# familia

class Familia(models.Model):
    n_familia = models.CharField(max_length=45)

    def __str__(self):
        return self.n_familia


class UsuarioFamilia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.familia}"

# eventos

class Evento(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(blank=True)  
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)  

    def __str__(self):
        return self.nombre
    
class UsuarioEvento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.familia}"
