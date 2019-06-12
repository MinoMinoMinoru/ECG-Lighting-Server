from datetime import datetime as dt

import sys
sys.path.append('../FileModule')
from FileModule.fileManager import *

def setTermData(term_rri, term_time,rri,time):
    ''' termに配列にデータを格納(term_rri,term_time,rri,now_time) '''
    if rri > 400 and rri < 1500:
        term_rri.append(rri)
        term_time.append(time)
    else:
        print("異常なRRIの値であるため，判定から外しました")

def outputRRI(time,rri,filename):
    ''' RRIをcsvに出力 '''
    output_text = makeRRILogTExt(time,rri)
    outputFile(output_text, filename)

def outputCVRR(count,time,cvrr,filename):
    ''' CVRRをcsvに出力 '''
    output_text = str(count) + "," +str(time) + "," + str(cvrr) + '\n'
    outputFile(output_text, filename)