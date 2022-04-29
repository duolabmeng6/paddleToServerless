# 飞桨模型使用ONNX推理

在使用飞桨训模型后，用飞桨推理非常方便。

但是需要安装 paddle 的推理库，体积就非常的大了~

本文介绍一种轻量的模型部署方式

# 目标

* 将飞桨训练好的模型转换为onnx模型
* 使用ONNX Runtime的框架推理



# ONNX是什么

https://onnx.ai/

ONNX (Open Neural Network Exchange) 是针对机器学习所设计的开源文件格式，用于存储训练好的模型。它使得不同的人工智能框架可以采用相同格式存储模型并交互。通过ONNX格式，Paddle模型可以使用OpenVINO、ONNX Runtime等框架进行推理。



# 飞桨模型模型导出ONNX协议

Paddle转ONNX协议由 [paddle2onnx](https://github.com/PaddlePaddle/paddle2onnx) 实现



```
pip install paddle2onnx onnx onnxruntime // -i https://mirror.baidu.com/pypi/simple 如果网速不好，可以使用其他源下载
```



# PaddleX模型转换为onnx

```
pip install paddle2onnx
```

```
paddle2onnx --model_dir C:\Users\csuil\paddlex_workspace\P0013-T0021_export_model\inference_model\inference_model  --model_filename model.pdmodel  --params_filename model.pdiparams --save_file onnx_file --opset_version 10 --enable_onnx_checker True
```





## 转换时常见问题帮助

### Q1: 转换出错，提示 "Converting this model to ONNX need with static input shape, please fix input shape of this model"

- 在某些场景下，模型的输入大小需要固定才能使用Paddle2ONNX成功转换，原因在于PaddlePaddle与ONNX算子上的差异。
- 例如对于图像分类或目标检测模型而言，[-1, 3, -1, -1]被认为是动态的输入大小，而[1, 3, 224, 224]则是固定的输入大小（不过大多数时候batch维并不一定需要固定， [-1, 3, 224, 224]很可能就可以支持转换了)
- 如果模型是来自于PaddleX，参考此[文档导出](https://github.com/PaddlePaddle/PaddleX/blob/develop/docs/apis/export_model.md)通过指定`--fixed_input_shape`固定大小
- 如果模型来自于PaddleDetection，参考此[文档导出](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.3/deploy/EXPORT_ONNX_MODEL.md)

### Q2: 转换出错，提示"Fixed shape is required, refer this doc for more information"

- 参考Q1的解决方法



# ONNXRuntime推理

[Paddle2.0导出ONNX模型和推理](https://aistudio.baidu.com/aistudio/projectdetail/1461212)

* 模型输入前的预处理
* 模型输出结果的处理

































