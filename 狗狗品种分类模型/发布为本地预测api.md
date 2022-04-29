# 使用paddleHUB 部署为本地预测api

https://github.com/PaddlePaddle/PaddleX/blob/develop/docs/hub_serving_deploy.md

* 1 转换模型
  
  hub convert --model_dir ./inference_model/inference_model --module_name gougoupinzhongshibie

* 2 安装模型

  hub install .\gougoupinzhongshibie_1650904537.2404501\gougoupinzhongshibie.tar.gz

* 3 部署为接口

  hub serving start --modules gougoupinzhongshibie -p 9000