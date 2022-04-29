docker build -f ./Dockerfile -t kunchongjiance:1.0 .
docker rm -f kunchongjiance
docker run -itd --name kunchongjiance -p 9022:9000 kunchongjiance:1.0 /bin/bash -c "sh /app/start.sh"
docker logs kunchongjiance
docker diff kunchongjiance

#没问题的话就可以执行推送命令
docker build -f ./Dockerfile -t kunchongjiance:1.0 .
docker tag kunchongjiance:1.0 registry.cn-shenzhen.aliyuncs.com/duolabmeng/kunchongjiance:1.16
docker push registry.cn-shenzhen.aliyuncs.com/duolabmeng/kunchongjiance:1.16