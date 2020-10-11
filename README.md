# Automobile comparator

The aim of this project is to provide an app that can scrappe data and, through a machine learning model, provides a second hand market valuation for any add according to its settings.

## Developpment  environnement

**Dockerfile** provides a simple container setup to deploy the project on developpment mode.
**docker-compose.yml** stores containers' orchestration for database and web server.

### Deployement
To create images and containers:
```bash
docker-compose up --build -d
```

To check the two containers (**runserver** and **database**) are running well:
```bash
docker ps
```

To migrate the database:
```bash
docker exec runserver ./manage.py migrate
```

To connect to the database without client (password: _root_):
```bash
docker exec -ti database mysql -u root -h localhost -p autodb
```
Then go to http://127.0.0.1:8080

### Re-build web-server
If a new commit has been done, here is a command that re-build the web-server without destroying the database
```bash
docker-compose build runserver
```
