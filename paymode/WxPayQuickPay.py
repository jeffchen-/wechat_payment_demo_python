#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from util.util import *
from config import WxPayConfig

class WxPayQuickPay:

     def __init__(self):
         self.parameters = {}
         self.parameters["appid"] = WxPayConfig.APPID  
         self.parameters["mch_id"] = WxPayConfig.MCH_ID  
         self.parameters["spbill_create_ip"] = WxPayConfig.SPBILL_CREATE_IP        
         self.parameters["nonce_str"] = createNoncestr() 
         self.parameters["out_trade_no"] = make_out_trade_no() 
         self.result = {}
         self.url = "https://api.mch.weixin.qq.com/pay/micropay"
         self.timeout = WxPayConfig.TIMEOUT 
         self.response = None
         self.xml = ""
         self.error = ""

    #传入可选可选参数
     def add_Optional_Params(self,key,value):
        if key not in ("device_info","detail","attach","fee_type","goods_tag","limit_pay"):
            raise ValueError("不支持的接口参数")
        self.parameters[key] = value;

    #必填参数中body，total_fee,auth_code是需要传入的，其他必填参数服务器配置或者生成
     def add_Required_Params(self,key,value):
        if key not in ("body","total_fee","auth_code"):
            raise ValueError("不支持的接口参数")
        self.parameters[key] = value;

    #打印当前所有参数
     def printiAllParams(self):
         for k,v in self.parameters.items():  
             print ("参数名: %s, 值: %s"% (k,v))

    #生成post的XML
     def createXml(self):
         if any(self.parameters[key] is None for key in ("out_trade_no", "body", "total_fee", "auth_code", "spbill_create_ip")):
             #Todo: add error log here
             raise ValueError("missing parameter")
         self.parameters["sign"] = makeSign(self.parameters) 
         self.xml = dictToXml(self.parameters)

    #提交刷卡支付
    #成功时: 返回刷卡支付回复或者查询订单回复
    #错误时：返回FALSE，错误信息在error中描述
     def quickPay(self):
         self.createXml()
         #if any(self.parameters[key] is None for key in ("out_trade_no", "body", "total_fee", "auth_code", "spbill_create_ip")):
         #    raise ValueError("提交被扫支付API接口中，缺少必填参数")
         print (self.xml)
         self.response = postXml(self.xml,self.url,5)
         print (self.response)
         #所有无需处理的错误情况都在payResult里直接抛出异常
         self.payResults()
         #成功直接返回
         if self.result["return_code"] == "SUCCESS":
             return self.result
         #其他情况都需要调用查询订单接口
         order_id = self.parameters["out_trade_no"]
         query_times = WxPayConfig.QUERY_TIMES
         query_interval = WxPayConfig.QUERY_INTERVAL
         while(query_times >0):
             query = WxPayQueryPay(order_id)
             query_result = query.queryPay() 
             if query_result == 1:
                 return query.result 
             elif query_result == 3:
                 sleep(query_interval)
                 continue
             else:
                 self.error = query.error
                 return False
             query_times = query_times - 1
         else:
             self.error = "支付失败，请重新下单"
             return False

    #提交刷卡支付回复处理
     def payResults(self):
         self.result = xmlToDict(self.response)
         if self.result["return_code"] != "SUCCESS":
             #异常处理，应该是15秒以后撤销订单
             raise ValueError("提交刷卡支付回复通信失败")
         if not checkSign(self.result):
             #异常处理，应该是15秒以后撤销订单
             raise ValueError("提交刷卡支付回复签名错误")
         if self.result["result_code"] == "FAIL" and self.result["err_code"] != "SYSTEMERROR" and self.result["err_code"] != "USERPAYING" and self.result["err_code"] != "BANKERROR":
             #记录失败的err_code 和 err_code_des,15秒后撤销订单
             raise ValueError("提交刷卡支付结果是失败")
         return

if __name__ == '__main__':
     test_quickpay = WxPayQuickPay()
     test_quickpay.add_Required_Params("body","测试".encode('utf-8'))
     test_quickpay.add_Required_Params("total_fee","1")
     auth_code = input("请输入微信支付条码:")
     test_quickpay.add_Required_Params("auth_code",auth_code)
     test_quickpay.quickPay()

