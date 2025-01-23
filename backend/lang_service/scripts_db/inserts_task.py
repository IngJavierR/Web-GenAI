import os
import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg2
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Configuración de la conexión a la base de datos
DB_NAME = os.environ.get('DATABASE')
DB_USER = os.environ.get('DBUSER')
DB_PASSWORD = os.environ.get('DBPASS')
DB_HOST = os.environ.get('IPDB')
DB_PORT = os.environ.get('DBPORT')

# Crear conexión con la base de datos
connection = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)
cursor = connection.cursor()

# Instanciar Faker
faker = Faker()

# Crear datos para la tabla areas
areas = [faker.company() for _ in range(5)]
area_ids = []
for area in areas:
    cursor.execute("""
    INSERT INTO areas (area_name) VALUES (%s) RETURNING area_id;
    """, (area,))
    area_ids.append(cursor.fetchone()[0])

# Crear datos para la tabla employees
employees = []
employee_ids = []
for _ in range(20):
    employee_name = faker.name()
    employee_age = random.randint(20, 60)
    area_id = random.choice(area_ids)
    cursor.execute("""
    INSERT INTO employees (employee_name, employee_age, area_id) VALUES (%s, %s, %s) RETURNING employee_id;
    """, (employee_name, employee_age, area_id))
    employee_ids.append(cursor.fetchone()[0])

# Crear datos para la tabla tasks
tasks = []
for _ in range(50):
    task_name = faker.sentence(nb_words=5)
    completed = random.choice([True, False])
    due_date = faker.date_between(start_date="-30d", end_date="+30d")
    completion_date = due_date if completed else None
    priority = random.randint(1, 5)
    employee_id = random.choice(employee_ids)
    cursor.execute("""
    INSERT INTO tasks (task_name, completed, due_date, completion_date, priority, employee_id)
    VALUES (%s, %s, %s, %s, %s, %s);
    """, (task_name, completed, due_date, completion_date, priority, employee_id))

# Confirmar los cambios y cerrar la conexión
connection.commit()
cursor.close()
connection.close()

print("Datos generados y cargados exitosamente en la base de datos.")
