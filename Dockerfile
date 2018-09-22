from ubuntu
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-raspi2/ppa
RUN apt-get update
RUN apt-get install -y libraspberrypi-bin

