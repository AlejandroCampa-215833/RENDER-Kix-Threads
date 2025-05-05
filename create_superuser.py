import os
import django
import sys

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kix_Threads.settings')
django.setup()

from django.contrib.auth.models import User
from django.db.utils import IntegrityError, OperationalError
from django.db import connection

# Verificar si todas las tablas necesarias existen
def check_tables_exist():
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Tablas disponibles: {tables}")
        return 'auth_user' in tables

# Obtener credenciales del entorno o usar valores predeterminados
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@kixthreads.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

# Crear superusuario si no existe
try:
    # Verificar si las tablas necesarias existen
    if not check_tables_exist():
        print("Error: La tabla auth_user no existe. Las migraciones pueden no haberse aplicado correctamente.")
        sys.exit(1)
        
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superusuario '{username}' creado exitosamente.")
    else:
        print(f"El superusuario '{username}' ya existe.")
except IntegrityError:
    print("Error al crear el superusuario. Posiblemente ya existe.")
except OperationalError as e:
    print(f"Error de base de datos: {e}")
    print("Las migraciones pueden no haberse aplicado correctamente.")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado: {e}")
    sys.exit(1)