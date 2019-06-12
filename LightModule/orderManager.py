""" 
cvrrをもとに，次の調光命令を管理する（予定）
"""
import random

from LightModule.lightingFunction import *

def randomChange(now_ill,now_temp):
    """ ランダムで照度・色温度を変更 """
    next_ill,next_temp = now_ill,now_temp
    order_list=["up_ill","down_ill","up_temp","down_temp"]
    walkflag = random.randint(0,len(order_list)-1)
    order=order_list[walkflag]
    if walkflag==0:
        next_ill = upIlluminance(now_ill)
    elif walkflag==1:
        next_ill = downIlluminance(now_ill)
    elif walkflag==2:
        next_temp = upTemp(now_temp)
    else:
        next_temp = downTemp(now_temp)
    return next_ill,next_temp