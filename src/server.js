// Import modules
var http = require("http");
var fs = require("fs");

// Path of DataRoot
var documentRoot = "..\\reports";

// Port
var port = 8890;

var server = http.createServer(function (req, res) {
  // Get input url
  var url = req.url;

  // Make file path
  var file = documentRoot + url;
  console.log(`Requiring file: ${file}`);

  // Read file and transform
  fs.readFile(file, function (err, data) {
    if (err) {
      // If Error occurs,
      // return 404 page
      res.writeHeader(404, {
        "content-type": 'text/html;charset="utf-8"',
      });
      res.write("<p>File not exists</p>");
      res.end();
    } else {
      // If No Error,
      // return file
      res.writeHeader(200, {
        "content-type": "application/json",
      });
      res.write(data);
      res.end();
    }
  });
});

server.listen(port);

console.log(`Server listens at ${port}`);
