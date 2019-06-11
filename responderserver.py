import json,random,socket,os,requests
from pathlib import Path
import responder
from datetime import datetime as dt
from pyfiglet import Figlet

from CalcModule.calculater import *
from CalcModule.termManager import *
# from FileModule.fileManager import *

def parentdir(path='.', layer=0):
    return Path(path).resolve().parents[layer]

BASE_DIR = parentdir(__file__,1)

api = responder.API(
    static_dir=str(BASE_DIR.joinpath('static')),
)

myport = 8000

class server:
    # RRIと取得時間
    term_time,term_rri = [],[]
    # 処理をするまでの間隔
    interval = 10
    # 時間周り
    pre_time, now_time = dt.now().strftime("%H:%M:%S"), 0
    all_cvrr =[]
    pre_cvrr, now_cvrr = 0, 0
    # csvに保存する際に誰のかを判断する用
    name =""
    # 照明制御に利用
    update_count=0

    # 出力file
    rri_file = "RRI_Log.csv"
    cvrr_file = "CVRR_Log.csv"

    def on_get(self, req, res):
        ''' GET '''
        # 一応こっちからURLを渡してみる（今のところ上手くいってなくてhtmlで直打ち）
        url="ws://"+getIp()+":"+str(myport)
        res.content = api.template("index.html", word="test",url=url,interval = self.interval,preCVRR = server.pre_cvrr,nowCVRR = "未計測",pretime=server.pre_time,static = True)

    async def on_post(self, req, resp):
        ''' POST '''
        # 調光アルゴリズム入れるならこのメソッド？
        async def judgeCVRR():
            ''' CVRRの判定 '''
            print("【pre_cvrr】",server.pre_cvrr)
            print("【now_cvrr】",server.now_cvrr)

            # CVRRが以前のものよりも上昇している場合
            if self.now_cvrr>server.pre_cvrr:
                f = Figlet(font="slant")
                msg = f.renderText("UP CVRR")
                print(msg)
            # CVRRが以前のものよりも下降している場合
            else:
                f = Figlet(font="slant")
                msg = f.renderText("DOWN CVRR")
                print(msg)

        async def update():
            ''' 経過時間の判定とその場合の処理 '''
            # print("now",self.now_time, " - pre",self.pre_time,"sub",str(getTime(self.now_time)-getTime(self.pre_time)))
            if(getTime(server.now_time)-getTime(server.pre_time) >= server.interval):
                print("--- Server Update ---")
                # updateの回数を更新
                server.update_count+=1
                
                # cvrrの更新・追加
                server.pre_cvrr = server.now_cvrr
                server.now_cvrr = getCVRR(server.term_rri)
                
                server.all_cvrr.append(getCVRR(server.term_rri))
                print("【all_cvrr】",server.all_cvrr)
                # CVRRの判定
                await judgeCVRR()
                # serverの "クラス変数" である pre_time を更新
                server.pre_time = dt.now().strftime("%H:%M:%S")
                outputRRI(server.term_time,server.term_rri,server.name+"_"+server.rri_file)
                outputCVRR(server.now_time,server.now_cvrr,server.name+"_"+server.cvrr_file)
                # termに依存する変数を初期化
                server.term_time.clear()
                server.term_rri.clear()

        # ここからPOSTの処理
        # Request body 取得
        data = await req.media()
        server.now_time = dt.now().strftime("%H:%M:%S")
        server.name = data['name']
        setTermData(server.term_rri,server.term_time,data['RRI'],server.now_time)
        # 経過時間に応じた処理
        await update()
        
def getIp():
    ''' Server(実行しているPC)のIP Addressを取得 '''
    # ホスト名を取得、表示
    host = socket.gethostname()
    print("------")
    print("host：", host)
    # ipアドレスを取得、表示
    ip = socket.gethostbyname(host)
    print("myIP：", ip)
    print("PORT:",myport)
    print("------")
    return ip
    
""" routing """
# mainのHTTPメソッド
api.add_route("/", server,static=True)
# endpointを変えてwebsocket用に開放している？
@api.route("/ws", websocket=True)
async def websocket(ws):
    ''' websocket　'''
    await ws.accept()
    while True:
        # awaitするためしゃあなし実装
        text = await ws.receive_text()
        print(text)
        body = {
            "word":"message from responder",
            "pretime":server.pre_time,
            "nowtime":dt.now().strftime("%H:%M:%S"),
            "precvrr":server.pre_cvrr,
            "nowcvrr":server.now_cvrr
        }
        # await ws.send_text(f"Hello!Client")
        await ws.send_json(body)
    await ws.close()

# @api.route("/upload")
# async def upload_file(req, resp):
#     @api.background.task
#     def process_data(data):
#         file=data['file']
#         f = open('./{}'.format(data['file']['filename']), 'wb')
#         f.write(file['content'])
#         f.close()

if __name__ == '__main__':
    api.run(address=getIp(), port=myport)