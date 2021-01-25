# stage 1 build
FROM golang:1.14.3-buster as builder
WORKDIR /go/src/app
COPY skel.go /go/src/app/
RUN go get github.com/dgrijalva/jwt-go
RUN go get github.com/tkanos/gonfig
RUN go get cloud.google.com/go/secretmanager/apiv1
RUN go get google.golang.org/genproto/googleapis/cloud/secretmanager/v1
RUN go build skel.go


# stage 2 build distrolles runtime time
FROM gcr.io/distroless/base
USER nobody:nobody

COPY config.json /config.json
COPY rsa-private.pem /rsa-private.pem

EXPOSE 8888
CMD ["/skel"]

# step 3 copy binary
COPY --from=builder /go/src/app/skel /

#RUN apt-get update -y && apt-get install ca-certificates ca-cacert -y
#COPY skel /skel
#COPY config.json /config.json
#COPY rsa-private.pem /rsa-private.pem
#CMD ["/skel"] 
#
