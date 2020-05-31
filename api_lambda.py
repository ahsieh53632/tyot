const AWS = require("aws-sdk");
const doClient = new AWS.DynamoDB.DocumentClient({region: 'ap-northeast-2'});


exports.handler = function(e, ctx, callback) {
    console.log(e)
    var type = e.type
    var street = e.street
    var from = e.from
    var to = e.to
    var params = ''
    
    if (type == 'all') {
        console.log('all')
        params = {
            TableName: "tyotdb",
            ProjectionExpression: "p_img, obj_img",
            FilterExpression: "#st = :stName",
            ExpressionAttributeNames:{
                "#st": "Street"
            },
            ExpressionAttributeValues: {
                ":stName": street
            }
        };
    } else {
        params = {
                TableName : "tyotdb",
                ProjectionExpression: "p_img, obj_img",
                FilterExpression: "#st = :stName AND #d BETWEEN :from AND :end",
                ExpressionAttributeNames:{
                    "#st": "Street",
                    "#d": "Date"
                },
                ExpressionAttributeValues: {
                    ":stName": street,
                    ":from": parseInt(from),
                    ":end": parseInt(to),
                }
            };
    }
    
    
    doClient.scan(params, onScan);
    async function onScan(err, data) {
        if(err) {
            callback(err, null)
        } else {
            console.log(data)
            callback(null, data)
        }
    };
    
}