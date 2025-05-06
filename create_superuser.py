import os
import django
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kix_Threads.settings')
django.setup()

from django.contrib.auth.models import User
from django.db.utils import IntegrityError, OperationalError
from django.db import connection
from django.core.exceptions import ValidationError

def create_superuser():
    # Obtener credenciales del entorno
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    try:
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            print(f"El superusuario '{username}' ya existe.")
            return
        
        # Crear superusuario
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"Superusuario '{username}' creado exitosamente.")

    except ValueError as e:
        print(f"Error de validación: {str(e)}")
        sys.exit(1)
    except IntegrityError:
        print("Error al crear el superusuario. Posiblemente ya existe.")
        sys.exit(1)
    except OperationalError as e:
        print(f"Error de base de datos: {str(e)}")
        print("Las migraciones pueden no haberse aplicado correctamente.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    create_superuser()