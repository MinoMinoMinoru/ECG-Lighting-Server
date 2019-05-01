import json,random,socket
import falcon 
from datetime import datetime as dt

from CalcModule.calculater import *
from CalcModule.termManager import *
from FileModule.fileManager import *
from WebPage.display import *

class MainServer(object):
    term_time = []
    all_rri, term_rri, all_cvrr = [], [], []

    interval = 1000
    pre_time, now_time = dt.now().strftime("%H:%M:%S"), 0
    pre_cvrr, now_cvrr = 0, 0

    def on_get(self, req, res):
        ''' display用のHTMLを作る(まだ作りかけ) '''
        # file = 'HTML/viewtest.html'
        file = 'HTML/public/index.html'
        res.status = falcon.HTTP_200
        res.content_type = 'text/html'
        with open(file, 'r',encoding="utf-8_sig") as f:
            res.body = f.read()

    def on_post(self, req, res):
        # postパラメーターを取得
        body = req.stream.read()
        data = json.loads(body)

        # パラメーターの取得
        # self.name = data['name']
        # self.now_time = data['time']
        self.now_time = dt.now().strftime("%H:%M:%S")
        setTermData(self.term_rri, self.term_time,data['RRI'],self.now_time)
        subtime = getTime(self.now_time)-getTime(self.pre_time)

        # 一定時間経過の処理（ファイル書き込みもここで）
        # 別のファイルでメソッド作成して，１行くらいで処理を済ませたい感 is ある
        if(subtime > self.interval):
            self.now_cvrr = getCVRR(self.term_rri)
            self.all_cvrr.append(self.now_cvrr)
            print("nowCVRR:",self.now_cvrr)
            self.pre_time = dt.now().strftime("%H:%M:%S")
            self.term_rri.clear()

        print(body)
        res.body = json.dumps(data)

class  Updater(object):
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        # self.smell

    def on_post(self, req, res):
        ''' display用のHTMLを作る(まだ作りかけ) '''
        # file = 'HTML/viewtest.html'


# declear
app = falcon.API()
app.add_route("/", MainServer())
app.add_route("/smellUpdate", Updater())
smell = 0
# app.add_route("/minomino/1111", HelloResource())

# 面倒なのでPCのIPを取得してぶち込む
def getIp():
    # ホスト名を取得、表示
    host = socket.gethostname()
    print("------")
    print("host：", host)
    # ipアドレスを取得、表示
    ip = socket.gethostbyname(host)
    print("myIP：", ip)
    print("------")
    return ip

# RRIをテストで入れる用
def testRRI():
    return random.randint(600, 1200)

if __name__ == "__main__":
    from wsgiref import simple_server
    # httpd = simple_server.make_server("192.168.1.52", 8000, app)
    httpd = simple_server.make_server(getIp(), 8000, app)
    httpd.serve_forever()