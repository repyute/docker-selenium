#FROM selenium/node-chrome:4.1.2-20220227
#FROM selenium/standalone-chrome:4.1.2
FROM seleniarm/standalone-chromium:4.1.2-20220227

LABEL authors=Reputians

USER 1200

RUN x11vnc -storepasswd secret /home/seluser/.vnc/passwd

#====================================
# Scripts to run Selenium Standalone
#====================================
COPY start-selenium-standalone.sh /opt/bin/start-selenium-standalone.sh
COPY start-xvfb.sh /opt/bin/

#COPY /opt/bin/noVNC/index.html ./vnc/vnc_inside.html
COPY ./vnc/vnc.html /opt/bin/noVNC/index.html
COPY ./vnc/pixel.png /usr/share/images/fluxbox/ubuntu-light.png
#==============================
# Supervisor configuration file
#==============================
COPY selenium.conf /etc/supervisor/conf.d/

# Copying configuration script generator
COPY generate_config /opt/bin/generate_config

# Boolean value, maps "--relax-checks"
ENV SE_RELAX_CHECKS true

EXPOSE 4444
