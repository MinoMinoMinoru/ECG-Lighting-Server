""" 
cvrrをもとに，次の調光命令を管理する（予定）
"""
import random

from LightModule.lightingFunction import *

def chengeLight(ill_index,temp_index,name):
    light_sig,ill,temp = getSignal(ill_index,temp_index)
    # lighting_by_signal(light_sig)
    return 0

def randomChange(now_ill,now_temp):
    """ ランダムで照度・色温度を変更 """
    next_ill,next_temp = now_ill,now_temp
    walkflag = random.randint(0,3)

    if walkflag==0:
        next_ill = upIlluminance(now_ill)
    elif walkflag==1:
        next_ill = downIlluminance(now_ill)
    elif walkflag==2:
        next_temp = upTemp(now_temp)
    else:
        next_temp = downTemp(now_temp)
    return next_ill,next_temp