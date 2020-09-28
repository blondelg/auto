FROM ubuntu:latest
MAINTAINER geoffroy
EXPOSE 8080
EXPOSE 50000
VOLUME /data
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y wget
RUN apt-get install -y ufw
RUN apt-get install -y curl
RUN apt-get install -y gnupg
RUN apt-get install -y openjdk-8-jdk
RUN wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | apt-key add -
RUN sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
RUN apt-get update
RUN apt-get install -y jenkins
RUN apt-get install -y systemctl
RUN apt-get install -y curl
RUN systemctl start jenkins
WORKDIR /home/ubuntu
