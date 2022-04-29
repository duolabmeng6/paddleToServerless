import time
import cv2
import numpy as np
import onnxruntime

def 输入图像预处理(输入数据):
    # 将输入数据转换为浮动32输入
    图像数据 = 输入数据.astype('float32')
    # 图像均值
    图像均值 = np.array([0.485, 0.456, 0.406])
    # 图像方差
    图像方差 = np.array([0.229, 0.224, 0.225])

    # 获得图像的矩阵用0填充
    标准图像数据 = np.zeros(图像数据.shape).astype('float32')
    # 图像归一化
    for i in range(图像数据.shape[0]):
        标准图像数据[i, :, :] = (图像数据[i, :, :] / 255 - 图像均值[i]) / 图像方差[i]

    # 添加输入通道
    标准图像数据 = 标准图像数据.reshape(1, 3, 224, 224).astype('float32')
    return 标准图像数据

def softmax(x):
    x = x.reshape(-1)
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def 加载标签数据():
    classes = None
    class_file = r".\labels.txt"
    with open(class_file, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    return classes


# 加载onnx模型
sess = onnxruntime.InferenceSession('onnx_file')
# 加载分类标签
分类标签 = 加载标签数据()
输入名称 = sess.get_inputs()[0].name
输出名称 = sess.get_outputs()[0].name
print('输入名称:', 输入名称)
print('输出名称:', 输出名称)

图像 = cv2.imread("Alaskan_malamute_00346.jpg")
# bgr 数据 转换为 rgb数据
图像 = cv2.cvtColor(图像, cv2.COLOR_BGR2RGB)
# 重置图像大小
图像 = cv2.resize(图像, (224, 224))  # shape (224, 224, 3)  对应轴0 1 2
图像数据 = np.array(图像).transpose(2, 0, 1)  # shape (3, 224, 224) 对应轴 2 1 0

输入数据图像 = 输入图像预处理(图像数据)

# 模型预测
start = time.time()
网络输出结果 = sess.run(output_names=None, input_feed={'image': 输入数据图像})
end = time.time()

print('ONNXRuntime 推理耗时: %.04f s' % (end - start))
print(网络输出结果)

res = softmax(np.array(网络输出结果)).tolist()
print('处理网络输出结果 softmax')
print(res)

# 获取最大值索引
idx = np.argmax(res)
print('图片分类为: ' + 分类标签[idx])

# argsort 从大到小排序
# flip 上下翻转

sort_idx = np.flip(np.argsort(res))
print('前5预测结果')
# print(分类标签[sort_idx[:5]])
for k in sort_idx[:5]:
    print(分类标签[k], "%.03f" % (res[k]))


图像 = cv2.cvtColor(图像, cv2.COLOR_BGR2RGB)
cv2.imshow("image",图像)
cv2.waitKey()
