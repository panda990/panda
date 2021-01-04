# -*- coding:UTF-8 -*-
#导入所有依赖包
import flask
import werkzeug
import os
import getConfig
import numpy as np
import execute
from PIL import Image
import werkzeug.utils
#初始化一个字典，用于存放从配置文件中获取的配置参数
gConfig = {}
#使用get_config方法从配置文件中获取配置参数
gConfig = getConfig.get_config(config_file='config.ini')

#创建一个flask wen应用，名称为imgClassifierWeb
app = flask.Flask("imgClassifierWeb")

#定义一个函数，初步处理获得数据并调用execute中的方法进行预存
def CNN_predict():
        global secure_filename
        #使用PIL中 的Image打开文件并获取图像文件中的信息
        img = Image.open(os.path.join(app.root_path, 'predict_img/'+secure_filename))
        img = img.resize([32,32])
        #将图像文件的格式转换为RGB
        img = img.convert("RGB")
        #分别获取r,g,b三元组的像素数据并进行拼接
        r, g, b = img.split()
        r_arr = np.array(r)
        g_arr = np.array(g)
        b_arr = np.array(b)
        img = np.concatenate((r_arr, g_arr, b_arr))
        #将拼接得到的数据按照模型输入维度需要转换为（32，32，3)，并对数据进行归一化
        image = img.reshape([1, 32, 32, 3])/255
        #调用execute中的predict方法进行预测
        predicted_class = execute.predict(image)
        print(predicted_class)
        #将预测结果返回并使用模板进行页面渲染
        return flask.render_template(template_name_or_list="prediction_result.html",
                                 predicted_class=predicted_class)



app.add_url_rule(rule="/predict/", endpoint="predict", view_func=CNN_predict)


def upload_image():
    global secure_filename
    if flask.request.method == "POST":  # 设置request的模式为POST
        img_file = flask.request.files["image_file"]  # 获取需要分类的图片
        secure_filename = werkzeug.secure_filename(img_file.filename)
        # from werkzeug.utils import secure_filename  # 生成一个没有乱码的文件名

        img_path = os.path.join(app.root_path, "predict_img/"+secure_filename)  # 获取图片的保存路径
        img_file.save(img_path)  # 将图片保存在应用的根目录下
        print("图片上传成功.")

        return flask.redirect(flask.url_for(endpoint="predict"))
    return "图片上传失败"

#增加upload路由，使用POST方法，用于文件的上窜
app.add_url_rule(rule="/upload/", endpoint="upload", view_func=upload_image, methods=["POST"])

def predirect_upload():
    return flask.render_template(template_name_or_list="upload_image.html")

"""
"""
app.add_url_rule(rule="/", endpoint="homepage", view_func=predirect_upload)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
