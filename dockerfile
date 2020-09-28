FROM ubuntu:latest
MAINTAINER geoffroy
EXPOSE 8080
EXPOSE 50000
VOLUME /data
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y wget
RUN apt-get install -y gnupg
RUN apt-get install -y openjdk-8-jdk
RUN apt-get install -y python3.8
RUN apt-get install -y python3-distutils
RUN wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | apt-key add -
RUN sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
RUN apt-get update
RUN apt-get install -y jenkins
RUN apt-get install -y systemctl
RUN apt-get install -y curl
RUN apt-get install -y git
RUN systemctl enable jenkins
WORKDIR /home/ubuntu
RUN git clone https://github.com/blondelg/auto.git
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py
RUN pip install virtualenv
RUN virtualenv venv
RUN /home/ubuntu/venv/bin/pip install -r auto/requirements.txt

RUN cat /var/lib/jenkins/secrets/initialAdminPassword
