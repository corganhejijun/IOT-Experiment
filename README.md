# IOT-Experiment
物联网技术集成与开发 实验

需要修改Android 和 Django 服务器对应的IP地址
Android IP:
webThread = new WebThread("http://192.168.2.131:8000/data?recv", webHandler);
服务器（本机），填写树莓派IP：
rts.get("http://192.168.137.244:5000" + "?op=" + request.GET['get'])
7_feedback.py 上传到树莓派 填写对应服务器IP（本机IP）
REMOTE_SERVER_URL = "http://192.168.137.1:8000/data"
