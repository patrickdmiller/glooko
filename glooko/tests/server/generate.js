const { promises: fs } = require("fs");
const { v4: uuidv4 } = require('uuid');
let pumpGuid = '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d' 
async function load_file(){
  let j = JSON.parse(await fs.readFile("views/api_histories.json", "utf-8"));
  console.log(j.histories.length)
  for(i=0; i < j.histories.length; i++){
    if( j.histories[i].guid){
      j.histories[i].guid = uuidv4()
    }
    if (j.histories[i].item  && j.histories[i].item.pumpGuid){
      j.histories[i].item.pumpGuid = pumpGuid
      j.histories[i].item.guid = j.histories[i].guid
    }
  }

  await fs.writeFile("views/api_histories_clean.json", JSON.stringify(j))
}

load_file()