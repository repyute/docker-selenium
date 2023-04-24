# Selenium standalone (VNC control via APIs)

## Commands

docker build -t node-chrome-standalone-vnc-api -f standalone_chrome_vnc_s3_webserver/Dockerfile .

docker build -t 686143527223.dkr.ecr.ap-south-1.amazonaws.com/selenium-service:1.0.0 -f standalone_chrome_vnc_s3_webserver/Dockerfile .
