const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const cors = require('cors');
const app = express();
const port = 3000;
const path = require('path');
const { spawn } = require('child_process');
// const path = require('path');
const { dir } = require('console');


const uri = "mongodb+srv://interview:12345@cluster0.1ahe7l7.mongodb.net/interview?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

app.use(express.json());
app.use(cors());
app.use(express.static('public'));

client.connect(err => {
  if (err) {
    console.error(err);
    res.status(500).json({ message: 'Error connecting to database' });
    return;
  }
  else {
    console.log('connected to db');
  }

  const collection = client.db("interview").collection("timestamps");
  const collection1 = client.db("interview").collection("questions");
  const collection3 = client.db("interview").collection("users");

  app.post('/ranques', (req, res) => {
    collection1.deleteMany({}, function (err, result) {
      if (err) throw err;
      console.log("Deleted questions documents");
    })

    const dbques = req.body.ques;


    //console.log("Number of documents in collection: " + count);

    collection1.insertOne({ ques: dbques }, function (err, result) {
      if (err) {
        console.error(err);
        res.status(500).json({ message: 'Error inserting data into database' });
        return;
      }

      console.log("questions document inserted");
      res.json({ message: 'random questions inserted successfully' });
    });

  });


  app.get('/delete',(req,res)=>{
    const pythonProcess = spawn('python',['delete.py']);
    pythonProcess.stdout.on('data',(data)=>{
      console.log(data.toString);
    });
    pythonProcess.stderr.on('data',data =>{
      console.log(data.toString);
    });
    res.send('deleted audio files');
  });

  
  app.get('/log',(req,res)=>{
    res.sendFile(path.join(__dirname+'popup.html'));
  })

  app.get('/start', (req, res) => {
    const pythonProcess = spawn('python', ['voicefrommeet.py']);
    pythonProcess.stdout.on('data', (data) => {
      console.log(data.toString());
    });
    pythonProcess.stderr.on('data', (data) => {
      console.error(data.toString());
    });
    res.send('started recording');
    console.log("stared.........................................................");
  });



  app.get('/iris', (req, res) => {
    const pythonProcess = spawn('python', ['iris_detection.py']);
    //const pythonProcess1 = spawn('python', ['app.py']);
    pythonProcess.stdout.on('data', (data) => {
      console.log(data.toString());
    });
    pythonProcess.stderr.on('data', (data) => {
      console.error(data.toString());
    });
    res.send('Python script iris             detection             started!');
  })

  app.get('/end', (req, res) => {
    // Execute the Python script only when the "start" button is clicked
    const pythonProcess = spawn('python', ['end.py']);
    //const pythonProcess1 = spawn('python', ['app.py']);
    pythonProcess.stdout.on('data', (data) => {
      console.log(data.toString());
    });
    pythonProcess.stderr.on('data', (data) => {
      console.error(data.toString());
    });
    res.send('Python script end started!');
    console.log("1 audio file");



  });

  app.get('/app', (req, res) => {
    const pythonProcess1 = spawn('python', ['app.py']);
    //const pythonProcess1 = spawn('python', ['app.py']);
    pythonProcess1.stdout.on('data', (data) => {
      console.log(data.toString());
    });
    pythonProcess1.stderr.on('data', (data) => {
      console.error(data.toString());
    });
    res.send('Python script app started!');
  })
  
});
app.get('/thread', (req, res) => {
  const pythonProcess1 = spawn('python', ['thread.py']);
  //const pythonProcess1 = spawn('python', ['app.py']);
  pythonProcess1.stdout.on('data', (data) => {
    console.log(data.toString());
  });
  pythonProcess1.stderr.on('data', (data) => {
    console.error(data.toString());
  });
  res.send('Python script thread started!');
})


app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});