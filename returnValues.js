const AWS = require('aws-sdk');
const db = new AWS.DynamoDB.DocumentClient({region:'eu-central-1'});


exports.handler = (event, context, callback) => {
    //get data from db
    const roomName = event.name;
    let params ={
        TableName: 'ROOMS',
        Limit: 100
    }
    
    
    db.scan(params, function(err,data){
            if(err){
                callback(err, null); 
            }else{

                callback(null, data.Items);
        }})

};
