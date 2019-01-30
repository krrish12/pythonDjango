var ws = null;
//setInterval(check, 5000);
check()

function check(){
	if(!ws || ws.readyState == 3) start();
}
function start(){
	var chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/users/');
	
    chatSocket.onmessage = function(e) {
		
        var data = JSON.parse(e.data);
        var message = data['message'];
		console.log("message from web socket client"+message);
        document.getElementById('userStatus').innerHTML = (message);
    };
	chatSocket.onopen = function(e){
		console.log("web scocket opened successfully");
		chatSocket.send(JSON.stringify({
            'message': ''
        }));
	};
	chatSocket.onerror = function(e){
		console.log("chat socket error");
	};
    chatSocket.onclose = function(e) {
        console.log('closed!');
      //reconnect now
     check();
    };
};