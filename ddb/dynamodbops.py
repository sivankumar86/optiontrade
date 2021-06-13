import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vanigam')

def addentry(item):
    table.put_item(
        Item=item
    )

def getentries():
    done = False
    start_key = None
    scan_kwargs={}
    rows=[]
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        rows.append(response)
        start_key = response.get('LastEvaluatedKey', None)
    return response