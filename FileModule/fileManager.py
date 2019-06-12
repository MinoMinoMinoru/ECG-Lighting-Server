import json

def outputFile(write_text, write_file):
    ''' ファイル書き込み '''
    write_file = './output/' +write_file
    with open(write_file,'a') as file:
        file.write(write_text)

def makeRRILogTExt(time,RRI):
    ''' RRI配列をLog出力するためにtextにぶち込む(一定時間ごとに行うので配列処理) '''
    text = ""
    i = 0
    for i in range(len(time)):
        text += str(time[i]) + "," + str(RRI[i]) + '\n'
    return text