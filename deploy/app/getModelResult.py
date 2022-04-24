# coding: utf8
import requests
import json
import cv2
import base64
import numpy as np
def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tostring()).decode('utf8')

def non_max_suppress(predicts_dict, threshold=0.2, nms_threshold=0.1):
    """
    implement non-maximum supression on predict bounding boxes.
    Args:
        predicts_dict: {"stick": [[x1, y1, x2, y2, scores1], [...]]}.
        threshhold: iou threshold
    Return:
        predicts_dict processed by non-maximum suppression
    """
    # 转换为矩阵容易计算
    newdata = []
    for v in predicts_dict:
        x1, y1, x2, y2, score, category_id = v['bbox'][0], v['bbox'][1], v['bbox'][2], v['bbox'][3], v[
            'score'], v['category_id']
        x2 = x1 + x2
        y2 = y1 + y2

        if threshold > score:
            continue

        newdata.append([x1, y1, x2, y2, score, category_id])

    if(len(newdata)==0):
        return []
    bbox_array = np.array(newdata, dtype=np.float)

    ## 获取当前目标类别下所有矩形框（bounding box,下面简称bbx）的坐标和confidence,并计算所有bbx的面积
    x1, y1, x2, y2, scores = bbox_array[:, 0], bbox_array[:, 1], bbox_array[:, 2], bbox_array[:, 3], bbox_array[:, 4]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    # print "areas shape = ", areas.shape

    ## 对当前类别下所有的bbx的confidence进行从高到低排序（order保存索引信息）
    order = scores.argsort()[::-1]
    # print("order", order)
    keep = []  # 用来存放最终保留的bbx的索引信息

    ## 依次从按confidence从高到低遍历bbx，移除所有与该矩形框的IOU值大于threshold的矩形框
    while order.size > 0:
        i = order[0]
        keep.append(i)  # 保留当前最大confidence对应的bbx索引

        ## 获取所有与当前bbx的交集对应的左上角和右下角坐标，并计算IOU（注意这里是同时计算一个bbx与其他所有bbx的IOU）
        xx1 = np.maximum(x1[i], x1[order[1:]])  # 当order.size=1时，下面的计算结果都为np.array([]),不影响最终结果
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        inter = np.maximum(0.0, xx2 - xx1 + 1) * np.maximum(0.0, yy2 - yy1 + 1)
        iou = inter / (areas[i] + areas[order[1:]] - inter)
        # print("iou ", iou)

        # print(np.where(iou <= threshold))  # 输出没有被移除的bbx索引（相对于iou向量的索引）
        indexs = np.where(iou <= nms_threshold)[0] + 1  # 获取保留下来的索引(因为没有计算与自身的IOU，所以索引相差１，需要加上)
        # print("indexs ", indexs)
        order = order[indexs]  # 更新保留下来的索引
        # print("order ", order)
        bbox = bbox_array[keep]
        predicts_dict = bbox.tolist()

    # 还原回去
    newdata = []
    for v in predicts_dict:
        x1, y1, x2, y2, score, category_id = v[0], v[1], v[2], v[3], v[4], int(v[5])
        x2 = x2 - x1
        y2 = y2 - y1
        newdata.append({
            'category_id': category_id, 'bbox': [x1, y1, x2, y2], 'score': score
        })

    return newdata


def postprocess(res, threshold=0.5, nms_threshold=0.1):
    xywh_results = non_max_suppress(res, threshold, nms_threshold)
    preds = []
    for xywh_res in xywh_results:
        xywh_res['category'] = xywh_res['category_id']
        xywh_res['bbox'] = [int(v) for v in xywh_res['bbox']]
        xywh_res['score'] = float('%.3f' % xywh_res['score'])
        preds.append(xywh_res)
    return xywh_results

def getResult(image, threshold=0.5, nms_threshold=0.1):
    # 获取图片的base64编码格式
    data = {'images': [image]}
    # 指定content-type
    headers = {"Content-type": "application/json"}
    # 发送HTTP请求
    url = "http://127.0.0.1:9000/predict/kunchongjiance"
    print(url)
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    # print(r.text)
    res = postprocess(r.json()["results"][0], threshold, nms_threshold)
    # print(res)
    # 打印预测结果
    return res
if __name__ == '__main__':
    img1 = cv2_to_base64(cv2.imread("static/test.jpg"))
    result = getResult(img1)
    print(result)
    # print(len(result))