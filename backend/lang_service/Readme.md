# Service langchain

## Build

```bash
docker build --tag lang-service .

docker run -d --rm -p 8095:8095 lang-service

docker run -d -p 8095:8095 lang-service


docker pull epsilla/vectordb
docker run -d -p 8899:8888 epsilla/vectordb

docker run --name postgres-ai -e POSTGRES_PASSWORD=admin -e POSTGRES_USER=admin -e POSTGRES_DB=pruebas -p 5432:5432 -d postgres

aws configure --profile genai-admin
region us-east-1

npm install
ng serve

docker pull postgres
docker run --name postgres-ai -e POSTGRES_PASSWORD=admin -e POSTGRES_USER=admin -e POSTGRES_DB=pruebas -p 5432:5432 -d postgres

aws configure --profile genai-admin
region us-east-1

npm install
ng serve
```

## Types

Database Catalog:
* itsm
* retail

KnowledgeBase Catalog:
* chatbot
* contentmanager