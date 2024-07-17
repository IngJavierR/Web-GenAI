# Service langchain

## Build

```bash
docker build --tag lang-service .

docker run -d --rm -p 8095:8095 lang-service

docker run -d -p 8095:8095 lang-service


docker pull epsilla/vectordb
docker run -d -p 8899:8888 epsilla/vectordb
```

## Types

Database Catalog:
* itsm
* retail

KnowledgeBase Catalog:
* chatbot
* contentmanager