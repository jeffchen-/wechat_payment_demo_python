#!/usr/bin/python3.4
# encoding: utf-8

from util.util import *

class WxPayQueryPay(object):

     def __init__(self,out_trade_no="",transaction_id=""):
         self.parameters = {}
         self.parameters["appid"] = WxPayConfig.APPID
         self.parameters["mch_id"] = WxPayConfig.MCHID
         self.parameters["nonce_str"] = createNoncestr()
         self.parameters["out_trade_no"] = out_trade_no
         self.parameters["transaction_id"] = transaction_id
         self.result = {}
         self.url = "https://api.mch.weixin.qq.com/pay/orderquery"
         self.response = None
         self.xml = ""
         self.error = ""

     def printiAllParams(self):
         for k,v in self.parameters.iteritems():
             print "参数名: %s, 值: %s"% (k,v)

     #建议使用out_trade_no， 而不是transaction_id
     def createXml(self):
         if all(self.parameters.get("key") is "" for key in ("out_trade_no","transaction_id")):
             self.error = "参数out_trade_no和transcation_id不能都为空"
             return False
         self.parameters["sign"] = makeSign(self.parameters)
         self.xml = dictToXml(self.parameters)
         return True

     #返回参数  0:订单查询失败  1: 订单成功  2：订单失败  3：需要继续查询 4: 已撤销REVOKED 5: 转入退款REFUND
     #注意查询订单的超时应该上层去控制，查询接口本身只做查询
     def queryPay(self):
         if not self.createXml():
             return 0
         self.response = postXml(self.xml,self.url,5)
         #所有查询失败的情况已经在queryResults中返回FALSE
         if not self.queryResults():
             return 0 
         if self.result["result_code"] == "SUCCESS":
             if self.result["trade_state"] == "SUCCESS":
                 return 1
             elif self.result["trade_state"] == "USERPAYING":
                 return 3
             elif self.result["trade_state"] == "CLOSED":
                 self.error = "CLOSED:订单状态已关闭"
                 return 2 
             elif self.result["trade_state"] == "REVOKED":
                 self.error = "REVOKED:订单状态已撤销"
                 return 4 
             elif self.result["trade_state"] == "NOTPAY":
                 self.error = "NOTPAY:订单状态未支付"
                 return 2 
             elif self.result["trade_state"] == "PAYERROR":
                 self.error = "payerror:支付失败"
                 return 2 
             elif self.result["trade_state"] == "REFUND":
                 self.error = "REFUND:订单转入退款"
                 return 5 
             else:
                 self.error = "未知错误"
                 return 2
         if self.result["result_code"] == "FAIL" and self.result["err_code"] == "SYSTEMERROR":    
             return 3


     def queryResults(self):
         self.result = xmlToDict(self.response)
         if self.result["return_code"] != "SUCCESS":
             self.error = "return_code is Fail and return_msg is " + self.result["return_msg"]
             return False
         if not checkSign(self.result):
             self.error = "查询订单回复签名错误"
             return False
         if self.result["result_code"] == "FAIL" and self.result["err_code"] != "SYSTEMERROR":
             self.error = "result_code is Fail and err_code_des is " + self.result["err_code_des"]
             return False
         return True

