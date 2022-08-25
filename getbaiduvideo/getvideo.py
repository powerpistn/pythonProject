import urllib.request
import urllib.parse
from lxml import etree
import re
import json
from bs4 import BeautifulSoup
import configparser
import requests
import time

from flask import Flask, jsonify  #jsonify不仅支持json返回，而且是content-type是application/json
from flask import request
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示

def get_pages(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    #请求对象的定制
    request = urllib.request.Request(url=url,headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    return html

def parse_page(keyword):
    result=[]
    flag=1
    i=0
    while flag==1:
        num=i*10
        url = "https://www.baidu.com/sf/vsearch?pd=video&tn=vsearch&ie=utf-8&wrsv_spt=10&wd="+urllib.request.quote(keyword)+"&pn="+str(num)
        print(url)
        html=get_pages(url)
        content = BeautifulSoup(html, 'lxml')
        result_list=content.find_all(class_='video_list video_short')
        print('正在爬取:{},共查询到{}个结果'.format(url, len(result_list)))
        for res in result_list:
            data = {}
            res_title=res.find_all(class_='small_img_con border-radius')
            #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            for link in res_title:
                #print(link['href'])
                sub_url=link['href']
                result.append(sub_url)
                #print("\n")
        if len(result_list)==10:
           i=i+1
        else:
           flag=0
    return result


@app.route('/api/engine/data',methods=["POST"])
def run():
    if request.method == 'POST':
        json_data = request.json
        #keyword=json_data["keyword"]
        config=configparser.ConfigParser()
        config.read('./config.ini')
        keyword_list=config.get("keyword","keyword_list").split()
        service=config.get("service","url")
        print(keyword_list)
        print(service)
        print(len(keyword_list))
        for keyword in keyword_list:
           print(keyword)
           res_list=parse_page(keyword)
           data={}
           data["data_set_id"]="01"
           data["data_source_id"]="02"
           data["des_id"]="03"
           for res in res_list:
              data["url"]=res
              res= requests.post(service,json=data)
              json_res=res.json()
              print(json_res)
              while json_res["code"]!=0:
                 time.sleep(5)                 
                 res= requests.post(service,json=data)
                 json_res=res.json()
                 print(json_res)
                
    return data



if __name__ == '__main__':
    app.run(port=8000)

