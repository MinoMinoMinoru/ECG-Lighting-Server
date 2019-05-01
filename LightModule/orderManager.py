""" 
cvrrをもとに，次の調光命令を管理する（予定）
"""
from LightModule.lightingFunction import *

def order(changenum,currentIll,currentTemp,pre_cvrr,cvrr):
    ''' 試行回数が n回以下なら照度を，以上なら色温度を変更 '''
    # いずれの場合も返り値は照度と色温度のindex
    if changenum>0:
        return 0
    else:
        return 0

def orderIllminance(pre_order,pre_cvrr,cvrr,currentIll):
    ''' 照度を変更する命令 '''
    order_list = ["up","down"]
    if pre_cvrr > cvrr:
        # 条件一致とかの分岐が必要?
        # 一回テキトーに埋めとく
        upIlluminance(currentIll)
    else:
        order = pre_order
    return order

def orderTemp(pre_order,pre_cvrr,cvrr,currentTemp):
    ''' 色温度を変更する命令 '''
    order_list = ["up","down"]
    if pre_cvrr > cvrr:
        # 一回テキトーに埋めとく
        order = order_list[0]
    else:
        order = pre_order
    return order