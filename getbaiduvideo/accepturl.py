from flask import Flask, current_app, redirect, url_for, request
import json
import requests
import time
import random
# 实例化app
app = Flask(import_name=__name__)

# 通过methods设置POST请求
@app.route('/getresult', methods=["POST"])
def json_request():

    # 接收处理json数据请求
    res = request.get_json()
    print(res)
    data={}
    data["code"]=0
    data["msg"]="成功"
    service="http://127.0.0.1:8000/api/engine/data"
#    requests.post(service,json=data)
    return data    

if __name__ == '__main__':
    app.run(debug=True)
