var express = require('express');
var router = express.Router();
var http = require('http');
var querystring = require('querystring');

/* GET home page. */
router.get('/', function(req, res, next) {
  if (req.query.recv){
    res.send({t:30,h:60});
    return;
  }
  var data = req.query.data;
  console.log("get data " + data);
  res.render('index');
});

router.post('/', function(req, res, next){
  var i = req.body.data;
  console.log("get post data:" + i)
  res.send({data: parseInt(i)+1});
});

router.get('/com', function(req, res, next){
  if (req.query.method){
    var data = req.query.data;
    if (req.query.method == 'get'){
      http.get('http://127.0.0.1:8000/com?data=' + data);
    }
    res.send("ok");
    return;
  }
  else if (req.query.data){
    var data = req.query.data;
    console.log("I'm nodejs received get data: " + data);
    res.send("ok");
    return;
  }
  res.render('communicate');
});

router.post('/com', function(req, res){
  if (req.body.method){
    var data = req.body.data;
    data = querystring.stringify({'data':data});
    if (req.body.method == 'post'){
      var options = {
        hostname: '127.0.0.1',
        port: 8000,
        path: '/com',
        method: 'POST',
        headers: {
          "Content-Type": 'application/x-www-form-urlencoded',
          "Content-Length": data.length
        }
      };
      var request = http.request(options, function(res){});
      request.write(data);
      request.end();
    }
  }
  else if (req.body.data){
    var data = req.body.data;
    console.log("I'm nodejs received post data: " + data);
  }
  res.send("ok");
});

module.exports = router;
