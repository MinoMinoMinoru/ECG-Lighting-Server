import json

def outputFile(write_text, write_file):
    ''' ファイル書き込み '''
    write_file = './output/' +write_file
    with open(write_file,'a') as file:
        file.write(write_text)
    # print("【"+ write_file +"】Write !!"+'\n')

def makeLightLogText(time,ill,temp):
    ''' 調光Logを出力するためにtextにぶち込む '''
    text = str(time) + "," + str(ill) + "," + str(temp) + '\n'
    return text

def makeRRILogTExt(time,RRI):
    ''' RRI配列をLog出力するためにtextにぶち込む(一定時間ごとに行うので配列処理) '''
    text = ""
    i = 0
    for i in range(len(time)):
        text += str(time[i]) + "," + str(RRI[i]) + '\n'
    return text

def getSetting(route,filename):
    ''' jsonファイルから情報取得 '''
    f = open(route+filename, 'r')
    json_body = json.load(f)
    f.close()
    return json_body