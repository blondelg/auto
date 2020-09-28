# Automobile comparator

The aim of this project is to provide an app that can scrappe data and, through a machine learning model, provides a second hand market valuation for any add according to its settings.

## Developpment  environnement

**dockerfile** provides a simple container setup to deploy the project on developpment mode.

To build the image, run :
```bash
docker build -t auto-server:1.0 .
```

To launch the container, run :
```bash
docker run -tid \
            --name auto-server \
            --rm \
            --volume data:/home/ubuntu \
            --publish 8080:8080 \
            --publish 50000:50000 \
            --cap-add=NET_ADMIN \
            --cap-add=NET_RAW \
            auto-server:1.0
```

To start jenkins service, run :
```bash
docker exec -ti auto-server systemctl start jenkins
```
Then go to http://127.0.0.1:8080
