#!/usr/bin/python3.4
#coding:utf-8

'''
@author JeffChen
wechat payment SDK
'''
#微信公众号ID，可以登录MP平台查看，也可以查看开通微信支付的邮件
APPID = "wxcbb01f7940a2c600"

#公众号支付授权获取用户信息接口需要使用，公众平台后台查看
APPSECRET = ""

#普通模式时候是普通商户号
MCH_ID = "1241530002"

#商户支付密钥Key。审核通过后，在微信发送的邮件中查看
KEY = "32068419850321541900000000000000"

#异步通知url
NOTIFY_URL = ""

#JSAPI路径

#获取access_token过程中的跳转uri，通过跳转将code传入jsapi支付页面
JS_API_CALL_URL = ""

#证书路径,注意应该填写绝对路径
SSLCERT_PATH = "../cert/apiclient_cert.pem"
SSLKEY_PATH = "../cert/apiclient_key.pem"

#=======【requests超时设置】===================================
TIMEOUT = 30

#查询订单次数
QUERY_TIMES = 10
#查询订单时间间隔
QUERY_INTERVAL = 2

#本机IP地址,从本机读取如果需要
SPBILL_CREATE_IP = "127.0.0.1"


