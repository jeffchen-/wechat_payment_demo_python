#!/usr/bin/python3.4
# encoding: utf-8


'''
Utility for wechat payment
'''
from config import WxPayConfig
import xml.etree.ElementTree as ET
import requests
import datetime
import random
import hashlib

#字符串去空
def trimString(value):
     if value is not None and len(value) == 0:
         value = None
     return value

#生成随机数
def createNoncestr(length = 32):
     chars = "abcdefghijklmnopqrstuvwxyz0123456789"
     strs = []
     for x in range(length):
         strs.append(chars[random.randrange(0, len(chars))])
     return "".join(strs)

#生成随机数字
def randomDigitals(length = 8):
     chars = "0123456789"
     strs = []
     for x in range(length):
         strs.append(chars[random.randrange(0, len(chars))])
     return "".join(strs)

#拼接参数
def toUrlParams(paraMap):
     slist = sorted(paraMap)
     buff = []
     for k in slist:
         v = paraMap[k]
         buff.append("{0}={1}".format(k, v))
     return "&".join(buff)

#obj类型是dict,生成密钥
def makeSign(obj):
     String = toUrlParams(obj)
     String = "{0}&key={1}".format(String,WxPayConfig.KEY)
     String = String.encode('utf-8')
     String = hashlib.md5(String).hexdigest()
     result = String.upper()
     return result

#字典转成XML格式
def dictToXml(arr):
     xml = ["<xml>"]
     for k, v in arr.items():
         if v.isdigit():
             xml.append("<{0}>{1}</{0}>".format(k, v))
         else:
             xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
     xml.append("</xml>")
     return "".join(xml)

#XML转成字典
#TODO: 如果输入不是XML格式
def xmlToDict(xml):
     data = {}
     root = ET.fromstring(xml)
     for child in root:
         value = child.text
         data[child.tag] = value
     return data

def postXml(xml, url, seconds=30):
     headers = {'Accept-Charset':'utf-8'}
     r = requests.post(url, data=xml, headers=headers, timeout=seconds)
     r.encoding = 'utf-8'
     return r.text

def postXmlSSL(xml, url, second=30):
     r = requests.post(url, data=xml, timeout=seconds, verify=WxPayConfig.SSLCERT_PATH)
     r.encoding = 'utf-8'
     return r.text

def make_out_trade_no():
     nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
     return WxPayConfig.MCH_ID+str(nowTime)+randomDigitals()

#检查密钥，obj类型是dict
def checkSign(obj):
     tmp = dict(obj) 
     del tmp['sign']
     sign = makeSign(tmp)
     if obj['sign'] == sign:
         return True
     return False

