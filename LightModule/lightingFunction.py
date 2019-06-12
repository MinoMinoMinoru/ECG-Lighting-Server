import json,random
from datetime import datetime as dt

from .ledsock import *
import sys
sys.path.append('../FileModule')
from FileModule.fileManager import *

illList =[]
tempList=[]
# 照度，色温度の段階
ill_MAX =4
temp_MAX =7

def lighting_by_signal(signal):
    ''' test用に急繕ったもの '''
    s = LedSocket()
    s.connect()
    s.sendAll(signal)
    s.close()

def testSend(red,green,blue,yellow):
    ''' 引数の信号値で1回調光（調光テスト用で本番環境では未使用） '''
    s = LedSocket()
    s.connect()
    test_signal=[red,green,blue,yellow]
    s.sendAll(test_signal)
    s.close()

def upIlluminance(curentIll):
    ''' 照度を１段階上げる '''
    # 上限を超えなければみたいな処理
    if curentIll < ill_MAX:
        nextIll = curentIll + 1
    else:
        nextIll = curentIll
        print("照度はこれ以上大きくなりません")
    return nextIll

def downIlluminance(curentIll):
    ''' 照度を１段階下げる '''
    if curentIll > 0:
        nextIll = curentIll - 1
    else:
        nextIll = curentIll
        print("照度はこれ以上小さくなりません")
    return nextIll

def upTemp(curentTmep):
    ''' 色温度を１段階上げる '''
    if curentTmep < temp_MAX:
        nextTemp = curentTmep + 1
    else:
        nextTemp = curentTmep
        print("色温度はこれ以上大きくなりません")
    return nextTemp

def downTemp(curentTmep):
    ''' 色温度を１段階下げる '''
    if curentTmep > 0:
        nextTemp = curentTmep - 1
    else:
        nextTemp = curentTmep
        print("色温度はこれ以上小さくなりません")
    return nextTemp

def outputLighting(count,time,ill,temp,filename):
    ''' 調光のログを書く '''
    output_text = str(count) + "," + str(time) + "," + str(ill) + "," + str(temp) + '\n'
    outputFile(output_text, filename)

def getSignal(ill_index,temp_index):
    ''' jsonファイルから信号値を設定 '''
    signal =[]
    # f = open('signal40.json', 'r',encoding="utf-8")
    f = open('./LightModule/signal40.json', 'r',encoding="utf-8")
    get_data = json.load(f)
    f.close()
    get_data=get_data[str(ill_index)][temp_index]
    print(get_data['comment']+"で点灯します")
    signal.append(get_data['red'])
    signal.append(get_data['green'])
    signal.append(get_data['blue'])
    signal.append(get_data['yellow'])
    return signal,get_data['illuminance'],get_data['temperature']