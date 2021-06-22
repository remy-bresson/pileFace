import uuid
import boto3
from botocore.exceptions import ClientError
import os
import logging
from Person import Person

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamoTable=""

def init():
    global dynamoDbTable 

    print('init')    
    dynamoTableName = os.environ.get('DYNAMO_TABLE_NAME')
    dynamodb = boto3.resource('dynamodb')
    dynamoDbTable = dynamodb.Table(dynamoTableName)
    print('FIN init')

init()


def check_if_item_exist(userUid):
    global dynamoDbTable 
    response = dynamoDbTable.get_item(Key={'userId':userUid})

    if 'Item' in response:
        return True
    else:
        return False

def lambda_handler(event, context):
    firstname=event['firstname']
    lastname=event['lastname']
    userUid=str(uuid.uuid4())

    p1=Person(firstname,lastname,10)
    p1.presentation()

    #Test if not already exist then regenerate until a good one
    isfree=False
    while not isfree:
        if check_if_item_exist(userUid):
            # uid alread exist
            logger.warn("user id {} already in use".format(userUid))
            userUid=str(uuid.uuid4())
        else:
            logger.info("{} is free user uid".format(userUid))
            isfree=True              

        
    logger.info('Creating user for {} {}. User uid will be {}' .format(p1.getFistname(),p1.getLastname(),userUid))
    dynamoDbTable.put_item(
       Item={
            'userId': userUid,
            'firstname': p1.getFistname(),
            'lastname': p1.getLastname(),
            'amount': p1.getAmount()
        }
    )

    logger.info('User credit for new user {} is {}'.format(userUid, p1.getAmount()))
    return userUid