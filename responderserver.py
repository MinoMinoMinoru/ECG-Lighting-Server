import json,random,socket,os,requests
from pathlib import Path
import responder
from datetime import datetime as dt
from pyfiglet import Figlet

from CalcModule.calculater import *
from CalcModule.termManager import *
from LightModule.lightingFunction import *
from LightModule.orderManager import *

def parentdir(path='.', layer=0):
    return Path(path).resolve().parents[layer]

BASE_DIR = parentdir(__file__,1)

api = responder.API(
    static_dir=str(BASE_DIR.joinpath('static')),
)

myport = 8000

class server:
    # 処理をするまでの間隔(second)
    interval = 60
    # RRIと取得時間
    term_time,term_rri = [],[]
    pre_time, now_time = dt.now().strftime("%H:%M:%S"), 0
    all_cvrr =[]
    pre_cvrr, now_cvrr = 0, 0
    # csvに保存する際に誰のRRI,lightingかを判断する用
    name =""
    # 照明制御に利用
    lighting_signal=[]
    now_ill_index,now_temp_index=0,0
    pre_ill_index,pre_temp_index=0,0
    ill_index,temp_index=0,0
    state=""
    # 実際の照度・色温度
    illuminance,temperature=0,0
    # CVRRの算出回数と最大回数（終了条件）
    update_count=0
    break_point=10
    loop_max=10

    # 出力file
    rri_file = "RRI_Log.csv"
    cvrr_file = "CVRR_Log.csv"
    lighting_file = "Lighting_Log.csv"

    # 300lx,2700Kで調光
    lighting_signal,illuminance,temperature=getSignal(ill_index, temp_index)
    lighting_by_signal(lighting_signal)

    pre_time=dt.now().strftime("%H:%M:%S")
    print("interval:",interval)

    def on_get(self, req, res):
        ''' GET '''
        # 一応こっちからURLを渡してみる（今のところ上手くいってなくてhtmlで直打ち）
        url="ws://"+getIp()+":"+str(myport)
        res.content = api.template("index.html", word="test",url=url,interval = self.interval,preCVRR = server.pre_cvrr,nowCVRR = "未計測",pretime=server.pre_time,static = True)

    async def on_post(self, req, resp):
        ''' POST '''
        async def judgeCVRR():
            ''' CVRRの判定と調光信号値の決定 '''
            # print("【all_cvrr】",server.all_cvrr)
            # print("【pre_cvrr】",server.pre_cvrr)
            # print("【now_cvrr】",server.now_cvrr)

            # CVRRが以前のものよりも上昇している場合
            if self.now_cvrr>server.pre_cvrr:
                ''' Randomに調光 '''
                msg = Figlet(font="slant").renderText("UP CVRR")
                print(msg)
                print("照明環境を変更します")
                server.state="up"
                # server.ill_index,server.temp_index = self.ill_index,self.temp_index
                server.pre_ill_index, server.pre_temp_index = server.now_ill_index, server.now_temp_index
                server.now_ill_index, server.now_temp_index = randomChange(server.pre_ill_index, server.pre_temp_index)
                
            # CVRRが以前のものよりも下降している場合
            else:
                ''' 前の照明環境に戻す '''
                msg = Figlet(font="slant").renderText("DOWN CVRR")
                print(msg)
                print("前の照明環境に戻します")
                server.state="down"
                # print("server_index:("+str(server.ill_index)+","+str(server.temp_index)+")")
                self.now_ill_index, self.now_temp_index = server.pre_ill_index, server.pre_temp_index
                server.pre_ill_index, server.pre_temp_index = server.now_ill_index, server.now_temp_index
                server.now_ill_index, server.now_temp_index = self.now_ill_index, self.now_temp_index
            if server.update_count==server.break_point:
                ''' ここから休憩(task2breakの実験でのみ) '''
                server.pre_ill_index, server.pre_temp_index =0,0
                server.now_ill_index, server.now_temp_index =0,0
            # server.ill_index,server.temp_index = self.ill_index,self.temp_index            
            # 調光信号値，実際の照度，色温度の取得
            self.lighting_signal,server.illuminance,server.temperature = getSignal(server.now_ill_index, server.now_temp_index)
            # 調光
            lighting_by_signal(self.lighting_signal)
            

        async def update():
            ''' 経過時間の判定とその場合の処理 '''
            if(getTime(server.now_time)-getTime(server.pre_time) >= server.interval):
                # updateの回数を更新
                server.update_count+=1
                
                # cvrrの更新・追加
                server.pre_cvrr = server.now_cvrr
                server.now_cvrr = getCVRR(server.term_rri)
                server.all_cvrr.append(getCVRR(server.term_rri))

                # CVRRの判定+調光信号値の変更
                await judgeCVRR()

                # serverの "クラス変数" である pre_time を更新
                server.pre_time = dt.now().strftime("%H:%M:%S")

                # output csv
                outputRRI(server.term_time,server.term_rri,server.name+"_"+server.rri_file)
                outputCVRR(server.update_count,server.now_time,server.now_cvrr,server.name+"_"+server.cvrr_file)
                outputLighting(server.update_count,server.now_time,server.illuminance,server.temperature,server.now_cvrr,server.state,server.name+"_"+server.lighting_file)
                
                # termに依存する変数を初期化
                server.term_time.clear()
                server.term_rri.clear()

                print("update_count",server.update_count)

        ''' ここからPOSTの処理 '''
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

if __name__ == '__main__':
    api.run(address=getIp(), port=myport)