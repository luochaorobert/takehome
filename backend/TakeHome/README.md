# OCR英文字母识别系统

## 1 功能介绍

本系统使用Django框架（版本2.2）开发，可对用户上传图片（支持jpg或png格式）中包含的字母进行OCR识别，以json格式返回识别结果，并将上传的图片和识别结果保存至后台服务器。主页可查看已上传图片的识别记录。


## 2 安装说明

开发使用 python3.7 mysql8.0，部署测试环境 centOS7.6

1. 下载项目文件`/backend/TakeHome`到你的系统

2. 新建虚拟环境，安装`requirements.txt`文件中的依赖包`pip install -r requirements.txt`

3. 图片字符识别使用`pytesseract`库，依赖`Tesseract`软件，具体安装方式自行查阅相关文档

4. 参考`/envs/.env.example`文件配置系统变量文件，并在`/backend/TakeHome/TakeHome/settings.py`文件中导入配置好的系统变量文件`env.read_env('envs/.env.example')`

5. 新建数据库并初始化`python manage.py makemigrations`、`python manage.py migrate`

6. 运行项目`python manage.py runserver`，访问系统
http://your_ip 

7. 可以使用`/backend/TakeHome/test_data`文件夹中的图片进行测试
