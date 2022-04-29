# 推理API接口 

[可视化示例](/index.html)

---



## 文件上传

* 接口地址： /put
* 请求类型：POST

| 参数  |  数据类型 | 描述 |
|:-----  |:-----|-----                           |
| image | buf | 表单文件上传
| threshold | int| 置信度 0.1 - 1
| nms_threshold | int| 极大值抑制 0.1 - 1

### 测试

<form action="put" method="post"  enctype="multipart/form-data">
    <input id="image" name="image" type="file" accept=".gif,.jpg,.jpeg,.png">
    置信度<input id="threshold" name="threshold" type="text" value="0.3">
    极大值抑制<input id="threshold" name="nms_threshold" type="text" value="0.1">
    <input type="submit" value="提交">
</form>

---

## base64
* 接口地址： /put_base64
* 请求类型：POST

| 参数  |  数据类型 | 描述 |
|:-----  |:-----|-----                           |
| data | string| base64编码 例如 data:image/png;base64,/9j
| threshold | int| 置信度 0.1 - 1
| nms_threshold | int| 极大值抑制 0.1 - 1

### 测试


<img src="" id="showImage" alt="">

<form action="put_base64" method="post">
<input type="file" id="imgTest" type="file" onchange="imgChange(event)" accept=".gif,.jpg,.jpeg,.png">
    base64
    <input type="text" id="data" name="data" value="">
    置信度<input id="threshold" name="threshold" type="text" value="0.3">
    极大值抑制<input id="threshold" name="nms_threshold" type="text" value="0.1">
    <input type="submit" value="提交">
</form>
<script>
    function imgChange(e) {
        var reader = new FileReader();
        reader.onload = (function (file) {
            return function (e) {
                document.getElementById("showImage").setAttribute("src",this.result);
                document.getElementById("data").setAttribute("value",this.result);
            };
        })(e.target.files[0]);
        reader.readAsDataURL(e.target.files[0]);
    }
</script>



---


### 返回结果

```
// http://127.0.0.1:9000/put_base64
[
    {
        "category_id":1,
        "bbox":[
            236,
            293,
            53,
            50
        ],
        "score":0.859,
        "category":1
    },
    {
        "category_id":3,
        "bbox":[
            338,
            320,
            48,
            30
        ],
        "score":0.843,
        "category":3
    },
    {
        "category_id":2,
        "bbox":[
            297,
            263,
            44,
            35
        ],
        "score":0.799,
        "category":2
    },
    {
        "category_id":0,
        "bbox":[
            363,
            222,
            37,
            66
        ],
        "score":0.782,
        "category":0
    },
    {
        "category_id":4,
        "bbox":[
            242,
            405,
            19,
            29
        ],
        "score":0.744,
        "category":4
    },
    {
        "category_id":4,
        "bbox":[
            431,
            259,
            23,
            14
        ],
        "score":0.703,
        "category":4
    },
    {
        "category_id":4,
        "bbox":[
            413,
            302,
            40,
            20
        ],
        "score":0.489,
        "category":4
    }
]
```

---
