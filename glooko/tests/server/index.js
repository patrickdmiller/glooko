const express = require("express");
const app = require("express")();
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const { promises: fs } = require("fs");

app.use(express.static("public"));
app.set('view engine', 'html');
app.engine('html', require('ejs').renderFile);
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);
app.use(bodyParser.json());
app.use(cookieParser());
const server = require('http').Server(app);

app.get('/api/v3/users/summary/histories', async (req, res)=>{
  console.log("parameters", req.query)
  let j = await fs.readFile("views/api_histories.json", "utf-8");
  res.json(JSON.parse(j))
})

app.post('/users/sign_in', (req, res)=>{
  console.dir(req.body)
  res.render('signin.html')
})


app.get('/users/sign_in', (req, res)=>{
  res.render('signin.html')

})

app.get('/history', (req, res)=>{
  res.render('history.html')
})

server.listen(3000);