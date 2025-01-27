# Service langchain

## Build

### Local Containers Up
```bash
docker pull epsilla/vectordb
docker run -d -p 8899:8888 epsilla/vectordb
docker run --name postgres-ai -e POSTGRES_PASSWORD=admin -e POSTGRES_USER=admin -e POSTGRES_DB=pruebas -p 5432:5432 -d postgres
```

### AWS Configure
```bash
aws configure --profile genai-admin
region us-east-1
```

### Front Install
```bash
cd frontend/GenAIFront
npm install
```

### Backend Install
```bash
cd backend/lang_service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### BD Scripts Install
```bash
[Crear BD products_inventory]
create database products_inventory;

[Crear BD resumes]
create database db_resumes;

[Crear BD Tablas en products_inventory]
Execute scripts_db/schema_products.sql

[Insertar Registros en products_inventory]
python scripts_db/inserts_products.py

[Crear BD Tablas en pruebas]
Execute scripts_db/schema_pruebas.sql

[Insertar Registros en pruebas]
python scripts_db/inserts_task.py

[Crear BD Tablas en db_resumes]
Execute scripts_db/schema_resumes.sql
```

## Deploy

### Frontend
```bash
cd frontend/GenAIFront
ng serve
```

### Backend
```bash
cd backend/lang_service
python main.py
```

## Types

Database Catalog:
* itsm
* retail
* people

KnowledgeBase Catalog:
* chatbot
* contentmanager