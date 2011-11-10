var createServer = require("http").createServer;
var sys = require("sys");
var url = require("url");
var qs = require("querystring")


var ser = exports;
var map = {};
ser.get = function(path, handler){
    map[path] = handler;
};
NOT_FOUND = "not found\n";

var beginTime = Math.floor((new Date(2011, 0)).getTime()/1000);
sys.puts("beginTime " + beginTime);

function notFound(req, res) {
    res.writeHead(404, {"Content-Type":"text/plain", "Content-Length":NOT_FOUND.length});
    res.end(NOT_FOUND)
}
var server = createServer(function(req, res){
    if(req.method === "GET" || req.method === "HEAD") {
        var handler = map[url.parse(req.url).pathname] || notFound;
        res.simpleText=function(code, body){
            res.writeHead(code, {"Content-Type":"text/plain", "Content-Length":body.length});
            res.end(body);
        };
        res.simpleJSON = function(code, obj){
            var body = new Buffer(JSON.stringify(obj));
            res.writeHead(code, {"Content-Type":"application/json", "Content-Length":body.length});
            try{
                res.end(body);
            }
            catch(err)
            {
                sys.puts("send error");
            }
        };
        handler(req, res);
    }
});
ser.listen=function(port, host){
  server.listen(port, host);
  sys.puts("Server at http://"+(host||"127.0.0.1")+":"+port.toString()+"/");
};

HOST = null;
port = 8003;

var channels = {};//cid channel
function createChannel(cid)
{
    var channel = channels[cid];
    if(channel)
        return channel;
    var channel = new function() {
        var messages = [];
        var callbacks = [];
        this.appendMessage = function(uid, name, type, text){
            uid = parseInt(uid, 10)
            switch(type){
            case "msg":
                sys.puts("<"+uid+">"+text);
                break;
            case "join":
                sys.puts(nick+" join");
                break;
            case "part":
                sys.puts(nick+" part");
                break;
            };
            cur = Math.floor((new Date()).getTime()/1000);
            m = [uid, name,  text, (cur - beginTime)];

            messages.push(m);
            while(callbacks.length>0){
                callbacks.shift().callback([m]);
            }
            while(messages.length > 100)
                messages.shift();
        };
        this.query=function(since, callback){
            var matching = [];
            for(var i = 0; i < messages.length; i++){
                var message = messages[i];
                if(message[3] > since) {
                    matching.push(message);
                }
            }

            if(since == 0 && matching.length == 0)
            {
		now = (new Date()).getTime()/1000 - beginTime;
	        now = Math.floor(now)
                welcome = [0, "系统", "欢迎加入聊天室，点击输入框发送消息", now]
 	        matching.push(welcome)   
            }
            if(matching.length > 0)//have message to send callback
                callback(matching);
            else
                callbacks.push({timestamp:new Date(), callback: callback});//no message just hold on 
        };
        setInterval(function(){//remove long callbacks
            var now = new Date();
            while(callbacks.length > 0 && now - callbacks[0].timestamp > 30*1000) {
                callbacks.shift().callback([]);//return empty message
            }
        }, 3000);
    };
    channels[cid] = channel;
    return channel;
}


ser.listen(Number(process.env.port||port), HOST);
//first time receive or send will join
ser.get("/send", function(req, res){
    var uid = qs.parse(url.parse(req.url).query).uid;
    var name = qs.parse(url.parse(req.url).query).name;
    var cid = qs.parse(url.parse(req.url).query).cid;
    var text = qs.parse(url.parse(req.url).query).text;
    sys.puts("send " + uid + " "+ name +" "+cid +" " + text);
    channel = createChannel(cid)
    channel.appendMessage(uid, name, "msg", text);
    res.simpleJSON(200, {result: "send suc"});
});
ser.get("/recv", function(req, res){
    if(!qs.parse(url.parse(req.url).query).since){
        res.simpleJSON(400, {error:"no since"});
        return;
    }
    var uid = qs.parse(url.parse(req.url).query).uid;
    var cid = qs.parse(url.parse(req.url).query).cid;
    var since = parseInt(qs.parse(url.parse(req.url).query).since, 10);
    sys.puts("recv "+uid+" "+cid);
    channel = createChannel(cid)
    channel.query(since, function(messages){//callback function
        res.simpleJSON(200, {messages: messages});
    });
});
