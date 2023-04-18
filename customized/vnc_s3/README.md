docker build -t selenium/node-chrome-vnc-s3-dev:repute-4.1.2-20220131 -f DockerfileVncPassword .  

docker tag  docker.io/selenium/node-chrome-vnc-s3-dev:repute-4.1.2-20220131 686143527223.dkr.ecr.ap-south-1.amazonaws.com/selenium-node-chrome:repute-vnc-s3-dev-4.1.2-20220131

docker push 686143527223.dkr.ecr.ap-south-1.amazonaws.com/selenium-node-chrome:repute-vnc-s3-dev-4.1.2-20220131


docker build -t 686143527223.dkr.ecr.ap-south-1.amazonaws.com/selenium-node-chrome:repute-vnc-s3-prod-4.1.2-20220131 -f DockerfileVncPassword .

docker tag  docker.io/selenium/node-chrome-vnc-s3-prod:repute-4.1.2-20220131 686143527223.dkr.ecr.ap-south-1.amazonaws.com/selenium-node-chrome:repute-vnc-s3-prod-4.1.2-20220131

docker push 686143527223.dkr.ecr.ap-south-1.amazonaws.com/selenium-node-chrome:repute-vnc-s3-prod-4.1.2-20220131
