const AWS = require('aws-sdk');
const db = new AWS.DynamoDB.DocumentClient({region:'eu-central-1'});


exports.handler = (event, context, callback) => {

    const roomname = event.name;
    const roomstate = event.state;
    const roomavailability = event.availability;

    var params = {
    Item: {
      'NAME': roomname,
      'STATE': roomstate,
      'STATUS': roomavailability},
    TableName: 'ROOMS'
    };
  
    db.put(params, function(err, data) {
      if (err) {
        callback(err, null); 
      } else {
        callback(null, data);
      }});
    
    
};
