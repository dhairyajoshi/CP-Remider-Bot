from keep_alive import keep_alive
import os
import discord
import requests
import json
from datetime import date,time
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
API= os.getenv('API_KEY')

client= discord.Client()

def get_contest(dte):
  url='https://clist.by:443/api/v2/contest/?limit=10&start__gt='+str(dte)+'T00%3A00%3A00&order_by=end&format=json'
  response =requests.get(url,headers={'Authorization':'ApiKey ' + API})
  json_data=json.loads(response.text)
  result=''
  for i in range(0,5): 
    name = json_data["objects"][i]['event']
    start=json_data['objects'][i]['start']
    duration=json_data['objects'][i]['duration']
    fs=str(start[0:10])+' '+str((int(start[11:13])+5)%24)+str(start[13:])
    participate=json_data['objects'][i]['href']

    if(int(duration)/(3600*24)>=1):
      duration=str(int(duration)/(3600*24))
 
    elif (int(duration)/3600):
      duration= str(int(duration)/(3600))

    result+=name+'\n'+'starts: '+fs+'\n'+'duration: '+duration +' hours\n'+'participate at: '+participate+'\n\n'

  return result


@client.event
async def on_ready():
  print(f'logged in as {client.user}')

@client.event
async def on_message(msg):
  if msg.author == client.user:
    return

  if msg.content == '$show':
    dte=date.today()
    first= get_contest(dte)
    await msg.channel.send(first)

  if msg.content.startswith('$show -d'):
    dte=msg.content.split('d')[1].strip()
    first= get_contest(dte)
    await msg.channel.send(first)

  if msg.content.startswith('$help'):
    info='I am a bot to help you remind about upcoming contests \nUse $show to show list of contests going on today \nUse $show -d yyyy-mm-dd to show list of contests on that particular date\nStill under development don\'t bully please'
    await msg.channel.send(info)

keep_alive()
client.run(TOKEN)
