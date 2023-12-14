import boto3
def prepareResponse(event, msgText):
    response = {
          "sessionState": {
            "dialogAction": {
              "type": "Close"
            },
            "intent": {
              "name": event['sessionState']['intent']['name'],
                  "state": "Fulfilled"
            }
          },
          "messages": [
           {
             "contentType": "PlainText",
             "content": msgText
            }
           ]
       }
     
    return response
def upload_todb(data_to_insert):
    dynamodb = boto3.resource('dynamodb')
    # Get the DynamoDB table
    table = dynamodb.Table("lex_result")
    for key, value in data_to_insert.items():
        if value.isdigit():
            data_to_insert[key] = int(value)
    
    # Insert data into DynamoDB
    table.put_item(Item=data_to_insert)

print("Data inserted into DynamoDB table successfully.")
     
def lambda_handler(event, context):
    slots_data = event['sessionState']['intent']["slots"]
    result = {key: value["value"]["originalValue"] for key, value in slots_data.items()}
    result["email_address"]= result["Contact"]
    upload_todb(result)
    print(result)
    response = prepareResponse(event, "Please wait while I look through my incantations")   
         
    return response