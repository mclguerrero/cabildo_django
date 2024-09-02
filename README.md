# Proyecto Cabildo

## Introduccion

El proyecto **Cabildo** es una aplicación web desarrollada en Django que gestiona eventos y usuarios. Está diseñado para proporcionar una administración eficiente de eventos y autenticación de usuarios con una interfaz basada en plantillas HTML.

## Tecnologías Utilizadas

- Python 
- Django 
- MySQL

## Instalación

### Pasos de Instalación

1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/proyecto_cabildo.git
cd proyecto_cabildo
```

2. Crea y activa un entorno virtual

```bash
python -m venv env
env\Scripts\activate
```

3. Erro al activar el entorno virtual?

* Abrir PowerShell como administrador

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

* Confirma y cierra PowerShell

4. Instala las dependencias

```bash
pip install -r requirements.txt
```

5. Configura la base de datos

6. Aplica las migraciones

```bash
python manage.py makemigrations 
python manage.py migrate
```

7.Inicia el servidor de desarrollo

```bash
python manage.py runserver
```

## Estructura del Proyecto

```bash
proyecto_cabildo/
├──.gitignore
├── env
└── media
│   └── eventos
│       └──eventos.jpg
├── CabildoGranPutumayo/
│   ├── __pycache__
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── main/
    ├── __pycache__
    ├── migrations/
    ├── static/
    │   └── img
    ├── templates/
    │   ├── bases
    │   │   └── etc.html
    │   ├── eventos
    │   │   └── etc.html
    │   ├── login
    │   │   └── etc.html
    │   └── usuarios
    │       └── etc.html
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── context_processors
    ├── forms
    ├── models.py
    ├── tests.py
    ├── url.py
    └── views.py

```