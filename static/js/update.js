$(function () {
  var POLLLING_INVERVAL_TIME_IN_MILLIS = 5000;//mSeconds
  (function polling() {
      connectWebScoket();
      window.setTimeout(polling, POLLLING_INVERVAL_TIME_IN_MILLIS);
  }());

  function connectWebScoket() {
      var urltext = "ws://192.168.1.7:8000/ws";
      console.log("url:", urltext);
      var sock = new WebSocket(urltext);

      // 接続
      sock.addEventListener('open', function (e) {
          console.log('Socket 接続成功');
      });

      // サーバーにデータを送る
      sock.onopen=function(event){
          sock.send('Webの表示を更新します');
      }

      // サーバーからデータを受け取る
      sock.addEventListener('message', function (e) {
          var res = JSON.parse(e.data);
          console.log(res);
          document.getElementById('title').innerText = res.word;
          document.getElementById('NowTIME').innerText = "NowTIME:"+res.nowtime;
          document.getElementById('PreTIME').innerText = "PreTIME:"+res.pretime;
          document.getElementById('NowCVRR').innerText = "NowCVRR:"+res.nowcvrr;
          document.getElementById('PreCVRR').innerText = "PreCVRR:"+res.precvrr;

      });

      document.addEventListener('DOMContentLoaded', function (e) {
          // // サーバーにデータを送る
          //     sock.send('Webの表示を更新します');
      });
  }
}); 