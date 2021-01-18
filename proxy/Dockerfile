FROM ubuntu:20.04
RUN apt-get update -y && apt-get install ca-certificates ca-cacert -y
COPY skel /skel
COPY config.json /config.json
COPY rsa-private.pem /rsa-private.pem
CMD ["/skel"] 

