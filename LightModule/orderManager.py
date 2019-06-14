""" 
cvrrをもとに，次の調光命令を管理する（予定）
"""
import random

from LightModule.lightingFunction import *

ill_MAX =4
temp_MAX =7

def randomChange(now_ill,now_temp):
    """ ランダムで照度・色温度を変更 """
    next_ill,next_temp = now_ill,now_temp
    order_list=["up_ill","down_ill","up_temp","down_temp"]
    
    # 絶対に照明が変わるようにする
    if now_ill == ill_MAX:
        print("delete up_ill")
        order_list.remove("up_ill")
    elif now_ill == 0:
        print("delete down_ill")
        order_list.remove("down_ill")
    if now_temp == temp_MAX:
        print("delete up_temp")
        order_list.remove("up_temp")
    elif now_temp == 0:
        print("delete down_temp")
        order_list.remove("down_temp")

    walkflag = random.randint(0,len(order_list)-1)
    order=order_list[walkflag]

    if order=="up_ill":
        next_ill = upIlluminance(now_ill)
    elif order=="down_ill":
        next_ill = downIlluminance(now_ill)
    elif order=="up_temp":
        next_temp = upTemp(now_temp)
    elif order=="down_temp":
        next_temp = downTemp(now_temp)
    
    return next_ill,next_temp