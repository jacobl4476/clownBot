# bot.py
import discord
import boto3
import json
with open('creds.json', 'r') as f:
    creds = json.loads(f.read())


TOKEN = creds["token"]

intents = discord.Intents.all()

client = discord.Client(intents=intents)

cringe = ["i mean"]

botoClient = boto3.client('dynamodb', 'us-east-1',
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"]
    )

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    mes = message.content.lower().strip()

    if mes[0] == '!':
        if mes.split(" ")[0] == '!clown':
            userID = str(message.author.id)
            response = botoClient.get_item(
                TableName='clownTable',
                Key={'user': {'S': userID}}
            )
            count = 0
            try:
                count = int(response['Item']['count']['N'])
            except Exception as e:
                print('ERROR/CLEAN USER', e)
            await message.reply("You've been :clown:ed " + str(count) + " time(s)")
    for s in cringe:
        if s in mes:
            try:
                if mes[mes.find(s)+len(s)].isalpha():
                    break
            except:
                pass
            userID = str(message.author.id)
            response = botoClient.get_item(
                TableName='clownTable',
                Key={'user': {'S': userID}}
            )
            count = 0
            try:
                count = int(response['Item']['count']['N'])
            except Exception as e:
                print('ERROR/NEW USER', e)
            botoClient.put_item(
                TableName='clownTable',
                Item={
                    'user': {'S': userID},
                    'count': {'N': str(count+1)}
                }
            )
            await message.add_reaction('\N{CLOWN FACE}')

client.run(TOKEN)