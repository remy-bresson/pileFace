import boto3
import os
import logging
import random
import simplejson as json
import decimal
from decimal import Decimal


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamoTable=""
clientDb=""

def init():
    global dynamoDbTable 
    global clientDb 

    print('init')    
    dynamoTableName = os.environ.get('DYNAMO_TABLE_NAME')
    dynamodb = boto3.resource('dynamodb')
    dynamoDbTable = dynamodb.Table(dynamoTableName)
    print('FIN init')

init()

def checkBet(bet):
    if bet != "pile" and bet != "face":     
        raise Exception('Vous devez jouer pile ou face') 

def checkAndUpdateAmount(uid,amount):
    response = dynamoDbTable.get_item(Key={'userId':uid})    
    userInfosDumped=json.dumps(response)
    userInfos=json.loads(userInfosDumped)
    
    userCurrentAmount=userInfos["Item"]["amount"]
    logger.info("User {} has currently {}$".format(uid,userCurrentAmount))
    
    if amount > userCurrentAmount:
        #user exced his credit, not able to play
        raise Exception('Pas assez d\'argent sur votre compte, votre solde est de {}.  \
Envoyer un paypal a ****@gmail.com avec votre uid en commentaire pour recrediter votre comte'.format(userCurrentAmount)) 
    else:
        # retire le montant du paris de son credit
        newAmount=userCurrentAmount - amount
        dynamoDbTable.update_item(
            Key={
            'userId': uid
            },
            UpdateExpression="set amount=:a",
            ExpressionAttributeValues={
            ':a': Decimal(newAmount)
        },
        ReturnValues="UPDATED_NEW"
        )

        return newAmount


def lambda_handler(event, context):
    uid=event['uid']

    logger.info("Input uid is {}".format(uid))

    bet=event['bet']    
    amount=int(event['amount'])

    checkBet(bet)
    currentAmount = checkAndUpdateAmount(uid,amount)

    tirage=random.uniform(0, 10.0)

    #Le casino est toujours gagnant
    if tirage > 7:
        #Gagne
        if bet=="face":
            resultatTirage="face"
        else:
            resultatTirage="pile"
        
        gain = amount * 2
        logger.info("Bravo vous gagner {} avec le tirage {} ".format(gain,tirage))
        currentAmount=currentAmount+gain
        dynamoDbTable.update_item(
            Key={
            'userId': uid
            },
            UpdateExpression="set amount=:a",
            ExpressionAttributeValues={
            ':a': Decimal(currentAmount)
        },
        ReturnValues="UPDATED_NEW"
        )
    else:
        #Perdu
        if bet=="face":
            resultatTirage="pile"
        else:
            resultatTirage="face"

        logger.info("Jouer encore {}".format(tirage))
    
    print('Nouveau montant sur le compte : {}$'.format(currentAmount))
    
    resultat={"currentAmount":currentAmount, "resultatTirage":resultatTirage}
    return resultat