# porpose
- POSTserverをPythonで作りたかった
    - sensing dataを残したいためcloudはやめといた
    - 以前に作った解析プログラムを流用するためにPythonを使用
- Frameworkのresponderを採用
    - falconも使ってみたけどwebsocketがなさそうで路線変更した

# How to Use
- serverを立てる際にはresponderserver.pyを起動
    - その際にIPは自動で取得される
    - ただしwebsocketに関してはまだ自動化出来てないので手動で変更（2019/5/1時点）

# Program
## server
- responder:こっち！

## FileModule:csvの出力関連
- filemanager:file出力関連のfunction.出力したいものごとにメソッドを作ってる()

## LightModule：LED調光関連
- ledsocket:KC111の調光用のModule．色々とアレやけど深く考えない
- lightingFunctions:sokcet使った調光処理をmethod化
- order:ここでどのように調光するか判断して↑のメソッドを使用する
- lightingtest:メソッドの調子確認用．システム稼働環境では不要

## CalcModule:CVRRやらの計算関連
- calculater:CVRRの計算や時間を計算できるintへ変換
- termManager:一定時間ごとに行う処理をメソッド化.CVRRのfile出力もここで呼び出す．