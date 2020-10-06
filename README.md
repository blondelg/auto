# Automobile comparator

The aim of this project is to provide an app that can scrappe data and, through a machine learning model, provides a second hand market valuation for any add according to its settings.

## Developpment  environnement

**dockerfile** provides a simple container setup to deploy the project on developpment mode.

To build the image, run :
```bash
docker build --no-cache -t auto-server:1.0 .
```

To launch the container, run :
```bash
docker run -tid \
            --name runserver \
	    --hostname runserver
            --rm \
            --volume data \
            --publish 8000:8000 \
            runserver:1.0
```

Then go to http://127.0.0.1:8080

To get Jenkins password, run :
```bash
docker exec auto-server cat /var/lib/jenkins/secrets/initialAdminPassword
```
