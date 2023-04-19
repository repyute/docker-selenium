#FROM selenium/standalone-chrome:4.1.2
FROM seleniarm/standalone-chromium:4.1.2-20220227
LABEL authors=Reputians

USER 1200

#RUN x11vnc -storepasswd prod-vnc-pass-dfdfdd-4699-975f-03ce33d5965c /home/seluser/.vnc/passwd

#====================================
# Scripts to run Selenium Standalone
#====================================
COPY node_chrome_vnc_s3/start-selenium-standalone.sh /opt/bin/start-selenium-standalone.sh

#==============================
# Supervisor configuration file
#==============================
COPY node_chrome_vnc_s3/selenium.conf /etc/supervisor/conf.d/

# Copying configuration script generator
COPY node_chrome_vnc_s3/generate_config /opt/bin/generate_config

USER root
RUN apt-get update
RUN wget https://go.dev/dl/go1.20.3.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.20.3.linux-amd64.tar.gz
RUN export PATH=$PATH:/usr/local/go/bin
RUN echo $(go version)
USER 1200

# Boolean value, maps "--relax-checks"
ENV SE_RELAX_CHECKS true

EXPOSE 4444
