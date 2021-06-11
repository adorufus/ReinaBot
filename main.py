import os
import discord
import requests
import json

from pygelbooru import Gelbooru

client = discord.Client()
token = os.getenv('BOT_TOKEN')
gelKey = os.getenv('GEL_KEY')
r34_base_url = "https://r34-json.herokuapp.com"
r34Prefix = "!r34"

#gelbooru stuff
gelbooru = Gelbooru(gelKey, 795144)

def getR34(tag):
  response = requests.get(r34_base_url + '/posts?tags=' + tag + '&limit=5')
  json_data = json.loads(response.text)
  # print(json_data)
  return json_data['posts']

def checkIndex(a_list, index):
  print(index < len(a_list))
  return index < len(a_list)

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))
  # getR34()

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith("!hello"):
    print('{user} sending hello..')
    await message.channel.send("Hi!")

  if message.content.startswith(r34Prefix):
    if checkIndex(message.content.split(' '), 1):
      arg = message.content.split(' ')[1]
      arg2 = message.content.split(' ', 2)[2]
      arg3 = arg2.split(' ')

      print(arg3)

      data = getR34(arg)

      print(arg2)
      if "-r" in message.content:
        result = await gelbooru.random_post(tags=arg3)
        await message.channel.send("searching random lewd image...")
        await message.channel.send(str(result))
        # for i in range(len(result)):
        #   await message.channel.send(str(result[i]))

      else:
        if len(data) == 0:
          await message.channel.send("No Result Found")
        else:
          await message.channel.send("ah, a hentai suggestion for you..")
          for i in range (len(data)):
            await message.channel.send(data[i]['file_url'])
    else:
      await message.channel.send("please enter the tags \n e.g: ```!r34 samsung```")
      
    

client.run(token)
