const image = document.getElementById('image');
const canvas = document.getElementById('canvas');
const dropContainer = document.getElementById('container');
const warning = document.getElementById('warning');
const fileInput = document.getElementById('fileUploader');

// const URL = "http://localhost:5000/api/"
// const URL = "http://192.168.163.132:5000/api/"


function GetUrlPara() {
    var protocol = window.location.protocol.toString();
    // var host =  window.location.host.toString();
    var host = document.domain.toString();
    var port = window.location.port.toString();
    // var url = protocol + '//' + host + ":9000/put_base64";
    var url = "/put_base64";
    return url;
}


const URL = GetUrlPara()

// alert(URL);


function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
};


function windowResized() {
    let windowW = window.innerWidth;
    if (windowW < 480 && windowW >= 200) {
        dropContainer.style.display = 'block';
    } else if (windowW < 200) {
        dropContainer.style.display = 'none';
    } else {
        dropContainer.style.display = 'block';
    }
}

['dragenter', 'dragover'].forEach(eventName => {
    dropContainer.addEventListener(eventName, e => dropContainer.classList.add('highlight'), false)
});

['dragleave', 'drop'].forEach(eventName => {
    dropContainer.addEventListener(eventName, e => dropContainer.classList.remove('highlight'), false)
});

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropContainer.addEventListener(eventName, preventDefaults, false)
});

dropContainer.addEventListener('drop', gotImage, false)

// send image to server, then receive the result, draw it to canvas.
function communicate(img_base64_url) {
    threshold_ = document.getElementById('threshold').value;
    nms_threshold = document.getElementById('nms_threshold').value;
    $.ajax({
        url: URL,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(
            {
                "data": img_base64_url,
                "threshold": threshold_,
                "nms_threshold": nms_threshold,
            }),
        dataType: "json"
    }).done(function (response_data) {
        document.getElementById("code").innerText = format(JSON.stringify(response_data), false)
        jQuery('#run').attr("disabled", false);
        jQuery('#run span').hide();
        console.log(response_data);
        drawResult(response_data);
    });
}

function format(txt, compress/*是否为压缩模式*/) {/* 格式化JSON源码(对象转换为JSON文本) */
    var indentChar = '    ';
    if (/^\s*$/.test(txt)) {
        alert('数据为空,无法格式化! ');
        return;
    }
    try {
        var data = eval('(' + txt + ')');
    } catch (e) {
        alert('数据源语法错误,格式化失败! 错误信息: ' + e.description, 'err');
        return;
    }
    ;
    var draw = [], last = false, This = this, line = compress ? '' : '\n', nodeCount = 0, maxDepth = 0;

    var notify = function (name, value, isLast, indent/*缩进*/, formObj) {
        nodeCount++;/*节点计数*/
        for (var i = 0, tab = ''; i < indent; i++) tab += indentChar;/* 缩进HTML */
        tab = compress ? '' : tab;/*压缩模式忽略缩进*/
        maxDepth = ++indent;/*缩进递增并记录*/
        if (value && value.constructor == Array) {/*处理数组*/
            draw.push(tab + (formObj ? ('"' + name + '":') : '') + '[' + line);/*缩进'[' 然后换行*/
            for (var i = 0; i < value.length; i++)
                notify(i, value[i], i == value.length - 1, indent, false);
            draw.push(tab + ']' + (isLast ? line : (',' + line)));/*缩进']'换行,若非尾元素则添加逗号*/
        } else if (value && typeof value == 'object') {/*处理对象*/
            draw.push(tab + (formObj ? ('"' + name + '":') : '') + '{' + line);/*缩进'{' 然后换行*/
            var len = 0, i = 0;
            for (var key in value) len++;
            for (var key in value) notify(key, value[key], ++i == len, indent, true);
            draw.push(tab + '}' + (isLast ? line : (',' + line)));/*缩进'}'换行,若非尾元素则添加逗号*/
        } else {
            if (typeof value == 'string') value = '"' + value + '"';
            draw.push(tab + (formObj ? ('"' + name + '":') : '') + value + (isLast ? '' : ',') + line);
        }
        ;
    };
    var isLast = true, indent = 0;
    notify('', data, isLast, indent, false);
    return draw.join('');
}

// handle image files uploaded by user, send it to server, then draw the result.
function parseFiles(files) {
    const file = files[0];
    const imageType = /image.*/;
    if (file.type.match(imageType)) {
        warning.innerHTML = '';
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
            image.src = reader.result;
            // send the img to server
            communicate(reader.result);

        }
    } else {
        setup();
        warning.innerHTML = 'Please drop an image file.';
    }

}

// call back function of drag files.
function gotImage(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 1) {
        console.error('upload only one file');
    }
    parseFiles(files);
}

// callback function of input files.
function handleFiles() {
    parseFiles(fileInput.files);
}

// callback fuction of button.
function clickUploader() {
    fileInput.click();
}

// draw results on image.
function drawResult(results) {

    canvas.width = image.width;
    canvas.height = image.height;
    ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(image, 0, 0);
    for (bboxInfo of results) {
        bbox = bboxInfo['bbox'];
        class_name = bboxInfo['category'];
        score = bboxInfo['score'];

        ctx.beginPath();
        ctx.lineWidth = "1";

        ctx.strokeStyle = "red";
        ctx.fillStyle = "red";

        ctx.rect(bbox[0], bbox[1], bbox[2], bbox[3]);
        ctx.stroke();

        ctx.font = "12px Arial";

        let content = class_name + " " + parseFloat(score).toFixed(2);

        y = bbox[1] + 12;
        drawFillRect(ctx, bbox[0], bbox[1], bbox[2], 16, "#000", "", "rgba(255, 255, 255, 0.5)")
        ctx.strokeStyle = "red";
        ctx.fillStyle = "red";
        ctx.fillText(content, bbox[0] + 4, y);
    }
    image.style.display = "none"
}

function drawFillRect(cxt, x, y, width, height, borderWidth, borderColor, fillColor) {

    cxt.lineWidth = borderWidth;
    cxt.fillStyle = fillColor;
    // cxt.strokeStyle = borderColor;

    cxt.fillRect(x, y, width, height);
    // cxt.strokeRect(x, y, width, height);
}


// 初始化函数
async function setup() {
    // Make a detection with the default image
    // detectImage();
    jQuery('#run').attr("disabled", true);
    jQuery('#run span').hide();
    jQuery('#run span').show();

    var canvasTmp = document.createElement("canvas");
    canvasTmp.width = image.width;
    canvasTmp.height = image.height;
    var ctx = canvasTmp.getContext("2d");
    ctx.drawImage(image, 0, 0);
    var dataURL = canvasTmp.toDataURL("image/png");
    communicate(dataURL)
}

setTimeout(function () {
    setup();
}, 5000)


function reload_put(v) {
    document.getElementById('threshold').value = v
    setup();
}


