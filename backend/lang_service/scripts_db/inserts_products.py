import os
import psycopg2
from psycopg2 import sql
from faker import Faker
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Datos de conexión
DB_NAME = os.environ.get('DATABASE')
DB_USER = os.environ.get('DBUSER')
DB_PASSWORD = os.environ.get('DBPASS')
DB_HOST = os.environ.get('IPDB')
DB_PORT = os.environ.get('DBPORT')

# Conectar a la base de datos
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Crear un cursor
cur = conn.cursor()

# Generador de datos de prueba en español
fake = Faker('es_ES')

# Lista de productos alimenticios para generar nombres realistas
productos_alimentos = [
    'Pan', 'Leche', 'Queso', 'Yogur', 'Mantequilla', 'Huevos', 'Arroz', 'Pasta', 'Carne',
    'Pollo', 'Pescado', 'Manzanas', 'Plátanos', 'Naranjas', 'Fresas', 'Zanahorias',
    'Tomates', 'Lechuga', 'Patatas', 'Cebollas'
]

# Insertar datos en la tabla Categorias
categorias = []
for _ in range(5):
    nombre = fake.word().capitalize()
    descripcion = fake.text()
    cur.execute("""
        INSERT INTO Categorias (nombre, descripcion)
        VALUES (%s, %s) RETURNING id_categoria
    """, (nombre, descripcion))
    id_categoria = cur.fetchone()[0]
    categorias.append(id_categoria)

# Insertar datos en la tabla Proveedores
proveedores = []
for _ in range(5):
    nombre = fake.company()
    contacto = fake.name()
    telefono = fake.phone_number()
    email = fake.email()
    cur.execute("""
        INSERT INTO Proveedores (nombre, contacto, telefono, email)
        VALUES (%s, %s, %s, %s) RETURNING id_proveedor
    """, (nombre, contacto, telefono, email))
    id_proveedor = cur.fetchone()[0]
    proveedores.append(id_proveedor)

# Insertar datos en la tabla Productos
productos = []
for _ in range(20):
    nombre = random.choice(productos_alimentos)
    descripcion = f'{nombre} fresco y de alta calidad.'
    precio = round(random.uniform(1.0, 50.0), 2)
    id_categoria = random.choice(categorias)
    id_proveedor = random.choice(proveedores)
    url = fake.url()
    cur.execute("""
        INSERT INTO Productos (nombre, descripcion, precio, id_categoria, id_proveedor, url)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_producto
    """, (nombre, descripcion, precio, id_categoria, id_proveedor, url))
    id_producto = cur.fetchone()[0]
    productos.append(id_producto)

# Insertar datos en la tabla Inventario
for _ in range(50):
    id_producto = random.choice(productos)
    cantidad = random.randint(1, 100)
    fecha_entrada = fake.date_between(start_date='-1y', end_date='today')
    fecha_salida = fecha_entrada + timedelta(days=random.randint(1, 30)) if random.choice([True, False]) else None
    ubicacion = fake.word().capitalize()
    cur.execute("""
        INSERT INTO Inventario (id_producto, cantidad, fecha_entrada, fecha_salida, ubicacion)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_producto, cantidad, fecha_entrada, fecha_salida, ubicacion))

# Cerrar comunicación con la base de datos
cur.close()
conn.commit()
conn.close()

print("Datos de prueba insertados con éxito.")
