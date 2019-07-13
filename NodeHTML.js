var http = require("http");
var fs = require("fs");
var path = require('path');
const PORT_A = 2222;

var server = http.createServer(function(req, res) {
    //if (req.url != '/favicon.ico') console.log('request was made: ' + req.url);
    res.writeHead(200, { 'Content-Type': 'text/html' });

    var index = fs.createReadStream(__dirname + '/website/index.html', 'utf8');
    var profile = fs.createReadStream(__dirname + '/website/profile.html', 'utf8');
    var count = fs.createReadStream(__dirname + '/website/count.html', 'utf8');
    var home = fs.createReadStream(__dirname + '/website/home.html', 'utf8');
    var calc = fs.createReadStream(__dirname + '/website/calculator.html', 'utf8');
    var bj = fs.createReadStream(__dirname + '/website/blackjack.html', 'utf8');

    if (req.url === '/index.html') index.pipe(res);
    else if (req.url === '/profile.html') profile.pipe(res);
    else if (req.url === '/count.html') count.pipe(res);
    else if (req.url === '/calculator.html') calc.pipe(res);
    else if (req.url === '/blackjack.html') bj.pipe(res);
    else if (req.url.match("\.css$")) {
        var cssPath = path.join(__dirname, 'public', req.url);
        var fileStream = fs.createReadStream(cssPath, "UTF-8");
        res.writeHead(200, { "Content-Type": "text/css" });
        fileStream.pipe(res);
    } else if (req.url.match("\.png$")) {
        var imagePath = path.join(__dirname, 'website/img', req.url);
        var fileStream = fs.createReadStream(imagePath);
        res.writeHead(200, { "Content-Type": "image/png" });
        fileStream.pipe(res);
    } else if (req.url.match("\.mp3$")) {
        var audioPath = path.join(__dirname, 'website', req.url);
        var fileStream = fs.createReadStream(audioPath);
        res.writeHead(200, { "Content-Type": "audio/mp3" });
        fileStream.pipe(res);
    } else home.pipe(res);
});

server.listen(PORT_A);
console.log("Go to localhost:" + PORT_A);