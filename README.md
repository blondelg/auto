# Automobile comparator

The aim of this project is to provide an app that can scrappe data and, through a machine learning model, provides a second hand market valuation for any add according to its settings.

## Developpment  environnement

**Dockerfile** provides a simple container setup to deploy the project on developpment mode.
**docker-compose.yml** stores containers' orchestration for database and web server.

To deploy the developpment environnement:
```bash
docker-compose up --build -d
```

Then go to http://127.0.0.1:8080
