https://github.com/PaddlePaddle/PaddleX/blob/develop/docs/hub_serving_deploy.md

* 1 转换模型
hub convert --model_dir ./inference_model/inference_model --module_name kunchongjiance

* 2 安装模型

hub install kunchongjiance_1650718404.429104/kunchongjiance.tar.gz

* 3 部署为接口

hub serving start --modules kunchongjiance -p 9000


# 将昆虫检测模型部署到 Serverless 

docker run -itd --name pyrun -p 9002:9000 -v C:/Users/csuil/paddlex_workspace/P0010-T0020_export_model/deploy/app:/app registry.cn-shenzhen.aliyuncs.com/duolabmeng/pyrun:paddlehub222 /bin/bash

docker exec -it pyrun  /bin/bash

pip install paddlex==2.1.0 -i https://mirror.baidu.com/pypi/simple

hub install /app/kunchongjiance.tar.gz

# 镜像制作好了 推送到阿里云的镜像仓库

经过不断的调试...最终我们没能在函数计算上启动2个http端口.
所以我决定...直接魔改hub serving start 的服务...
最终我们只跟以前一样 在 start.sh中
直接运行 hub serving start -m kunchongjiance -p 9000 即可

构建好了 我们去函数计算跑一下把 应该是可以成功了~

# 部署到函数上


window上使用s deploy 经常有问题...

我们换到mac上执行...

也可以直接在阿里云的函数计算上直接创建函数










