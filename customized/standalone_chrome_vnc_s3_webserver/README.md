# Selenium standalone (VNC control via APIs)

## Commands

Linux:

docker build -t node-chrome-standalone-vnc-api -f standalone_chrome_vnc_s3_webserver/Dockerfile .

aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 686143527223.dkr.ecr.ap-south-1.amazonaws.com
docker build -t 686143527223.dkr.ecr.ap-south-1.amazonaws.com/selenium-service:1.0.0 -f standalone_chrome_vnc_s3_webserver/Dockerfile .
docker push 686143527223.dkr.ecr.ap-south-1.amazonaws.com/selenium-service:1.0.0

ARM:
docker buildx build -t 686143527223.dkr.ecr.ap-south-1.amazonaws.com/selenium-service:1.0.3 --platform linux/arm64 --no-cache -f standalone_chrome_vnc_s3_webserver/Dockerfile_localvnc .
docker-compose -f docker-compose-arm.yml down
docker build --pull --no-cache -t node-chrome-standalone-vnc-api-arm -f standalone_chrome_vnc_s3_webserver/Dockerfile_arm .
