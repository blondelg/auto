# Staring image
FROM python:3.8
MAINTAINER geoffroy

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ports exposure
EXPOSE 8000
VOLUME /data

# Setup python dependancies
RUN mkdir auto
WORKDIR /auto
COPY . /auto/
RUN cd /auto
RUN echo "DEBUG COPY CHECK"
RUN ls -l
RUN pip install --no-cache-dir -r requirements.txt

# Build the secret key generator
RUN echo "import random" > generate_key.py
RUN echo "print(''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@$^&*(-_=+)') for i in range(50)))" >> generate_key.py

# Setup environment configuration
RUN cp config/config_sample.ini config/config.ini
RUN sed -i "s/SECRET_KEY_PATTERN/$(python generate_key.py)/gI" config/config.ini
RUN sed -i "s/django.db.backends.sqlite3/django.db.backends.mysql/gI" config/config.ini
RUN sed -i 's|{BASE_DIR}/db.sqlite3|autodb|gI' config/config.ini
RUN sed -i "s/USER_PATTERN/root/gI" config/config.ini
RUN sed -i "s/PASSWORD_PATTERN/root/gI" config/config.ini
RUN sed -i "s/HOST_PATTERN/database/gI" config/config.ini
RUN sed -i "s/PORT_PATTERN/3306/gI" config/config.ini
RUN echo "DISPLAY CONFIG FILE"
RUN cat config/config.ini
# Start service when runs
# CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
