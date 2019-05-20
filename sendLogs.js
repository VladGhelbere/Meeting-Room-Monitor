const AWS = require('aws-sdk');
const db = new AWS.DynamoDB.DocumentClient({region:'eu-central-1'});


exports.handler = (event, context, callback) => {
    const id = Date.now();
    const room = event.room;
    const date = event.date;
    const trigger_hour = event.trigger_hour;
    const trigger_end_hour = event.trigger_end_hour;
    const number_of_persons = event.number_of_persons

    var params = {
    Item: {
      'ID': id,
      'ROOM': room,
      'DATE': date,
      'TRIGGER_HOUR': trigger_hour,
      'TRIGGER_END_HOUR': trigger_end_hour,
      'NUMBER_OF_PERSONS': number_of_persons},
    TableName: 'LOGS'
    };
  
    db.put(params, function(err, data) {
      if (err) {
        callback(err, null); 
      } else {
        callback(null, data);
      }});
    
};
