# Staring image
FROM python:3.8
MAINTAINER geoffroy

# Ports exposure
EXPOSE 8000
VOLUME /data

# Install dependancies
RUN apt-get update && apt-get install -y \
	vim \
	git \
	&& rm -rf /var/lib/apt/lists/*

# Setup python dependancies
RUN git clone https://github.com/blondelg/auto.git
WORKDIR /auto
RUN cd /auto
RUN pip install --no-cache-dir -r requirements.txt

# Build the secret key generator
RUN echo "import random" > generate_key.py
RUN echo "print(''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@$^&*(-_=+)') for i in range(50)))" >> generate_key.py

# Setup environment configuration
RUN cp auto/config_sample.ini auto/config.ini
RUN sed -i "s/SECRET_KEY_PATTERN/$(python generate_key.py)/gI" auto/config.ini
RUN sed -i "s/django.db.backends.sqlite3/django.db.backends.mysql/gI" auto/config.ini
RUN sed -i 's|{BASE_DIR}/db.sqlite3|autodb|gI' auto/config.ini
RUN sed -i "s/USER_PATTERN/root/gI" auto/config.ini
RUN sed -i "s/PASSWORD_PATTERN/root/gI" auto/config.ini
RUN sed -i "s/HOST_PATTERN/database/gI" auto/config.ini
RUN sed -i "s/PORT_PATTERN/3306/gI" auto/config.ini

# Start service when runs
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
