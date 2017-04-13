var express = require("express");
var handlebars = require("express-handlebars");

var app = express();
app.engine("handlebars", handlebars());
app.set("view engine", "handlebars");

app.get("/", function(req, res) {
  res.render("index", {
    title: "Ubi the Discord Bot",
    text: "Handlebars.js Success!"
  });
});

app.listen(3000, function() {
  console.log("Server started on port 3000");
});
