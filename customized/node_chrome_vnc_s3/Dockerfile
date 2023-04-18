FROM seleniarm/node-chrome:4.1.2-20220217
LABEL authors=Reputians

USER 1200

RUN x11vnc -storepasswd prod-vnc-pass-dfdfdd-4699-975f-03ce33d5965c /home/seluser/.vnc/passwd

#====================================
# Scripts to run Selenium Standalone
#====================================
COPY start-selenium-standalone.sh /opt/bin/start-selenium-standalone.sh

#==============================
# Supervisor configuration file
#==============================
COPY selenium.conf /etc/supervisor/conf.d/

# Copying configuration script generator
COPY generate_config /opt/bin/generate_config

# Boolean value, maps "--relax-checks"
ENV SE_RELAX_CHECKS true

EXPOSE 4444
