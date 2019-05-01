import os, json
from statistics import mean,stdev

def getTime(time_str):
    ''' 時間をintに変更(単位は秒[s]) '''
    time = time_str.split(':')
    time = calcSec(int(time[0]),int(time[1]),int(time[2]))
    return time

def calcMin(hour,minute):
    ''' "10:40"の表記を"640 分(min）" 換算に変換 '''
    return int(hour)*60 + int(minute)

def calcSec(hour,minute,second):
    ''' "10:40"の表記を"640 分(min）" 換算に変換 '''
    return int(hour)*60*60 + int(minute)*60 + int(second)

def calcTime(time):
    ''' "640"の表記を"10:40" に変換 '''
    hour = int(time/60)
    minute = int(time%60)
    if minute<10:
        minute = "0"+str(minute)
    return str(hour)+":"+str(minute)

def getCVRR(input_RRI):
    '''平均，標準偏差，CVRRを返す'''
    return 100*stdev(input_RRI)/mean(input_RRI)