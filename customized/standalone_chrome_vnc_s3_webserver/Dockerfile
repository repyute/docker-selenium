FROM golang:latest as builder
#docker build -f drogan/Dockerfile --build-arg ENV=qa .
RUN apt-get update
RUN apt-get install -y build-essential
#copy all private reposotory mentioned in go module
WORKDIR /go/repute.net/selenium_webserver
COPY selenium_webserver/go.mod .
COPY selenium_webserver/go.sum .
RUN go mod download
COPY selenium_webserver .
RUN GOOS=linux GOARCH=amd64 go build -ldflags="-w -s"

FROM selenium/standalone-chrome:4.1.2
#FROM seleniarm/standalone-chromium:4.8.3
LABEL authors=Reputians

USER 1200

#RUN x11vnc -storepasswd prod-vnc-pass-dfdfdd-4699-975f-03ce33d5965c /home/seluser/.vnc/passwd

#====================================
# Scripts to run Selenium Standalone
#====================================
COPY standalone_chrome_vnc_s3_webserver/start-selenium-standalone.sh /opt/bin/start-selenium-standalone.sh

#==============================
# Supervisor configuration file
#==============================
COPY standalone_chrome_vnc_s3_webserver/selenium.conf /etc/supervisor/conf.d/

# Copying configuration script generator
COPY standalone_chrome_vnc_s3_webserver/generate_config /opt/bin/generate_config

COPY standalone_chrome_vnc_s3_webserver/webserver.sh /opt/bin/webserver.sh

#COPY standalone_chrome_vnc_s3_webserver/config.toml /opt/selenium/config.toml

COPY ./standalone_chrome_vnc_s3_webserver/vnc/vnc.html /opt/bin/noVNC/index.html
COPY ./standalone_chrome_vnc_s3_webserver/vnc/pixel.png /usr/share/images/fluxbox/ubuntu-light.png

#USER root
#RUN apt-get update
#RUN wget https://go.dev/dl/go1.20.3.linux-amd64.tar.gz
#RUN tar -C /usr/local -xzf go1.20.3.linux-amd64.tar.gz
#RUN export PATH=$PATH:/usr/local/go/bin
#RUN echo $(go version)
USER 1200
COPY --from=builder /go/repute.net/selenium_webserver/selenium_webserver /app/selenium_webserver

# Boolean value, maps "--relax-checks"
ENV SE_RELAX_CHECKS true

EXPOSE 4444
EXPOSE 8080

CMD ["/opt/bin/entry_point.sh"]
