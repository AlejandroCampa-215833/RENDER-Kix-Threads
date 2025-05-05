import psycopg2
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Conectar a la base de datos
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("¡Conexión exitosa!")
    
    # Crear un cursor para ejecutar consultas SQL
    cursor = connection.cursor()
    
    # Consulta de ejemplo
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Hora actual:", result)

    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()
    print("Conexión cerrada.")

except Exception as e:
    print(f"Error al conectar: {e}")