import os
import discord
import json
import requests
import random
from newsapi import NewsApiClient
import time
from keep_alive import keep_alive

token = os.environ['token']# using env variable to store bot token
client=discord.Client()

def get_news(option):# gets the news content from news API
  newsapi = NewsApiClient(api_key='7d2c681aef4844cfa4048fddbfc5b6b9')
  top_headlines = newsapi.get_top_headlines(
  category=f'{option.lower()}', language='en', country='in')
  Headlines = top_headlines['articles']
  if Headlines:
		  for articles in Headlines:
			  b = articles['title'][::-1].index("-")
			  if "news" in (articles['title'][-b+1:]).lower():
			  	return(
				  	f"{articles['title'][-b+1:]}: {articles['title'][:-b-2]}.")
			  else:
				  return(
					f"{articles['title'][-b+1:]} News: {articles['title'][:-b-2]}.")
  else:
    return("Sorry no articles found on this topic")


def motivate(): # this function sends quotes from api to motivate a person
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def riddles(): # this fucntion asks riddles from a set riddles in the dictionary
  riddle={'egg':'What has to be broken before you can use it?','candle':'I’m tall when I’m young, and I’m short when I’m old. What am I?','sponge':'What is full of holes but still holds water?','promise':'What can you break, even if you never pick it up or touch it?','age':'What goes up but never comes down?','towel':'What gets wet while drying?','bank':'I have branches, but no fruit, trunk or leaves. What am I?','echo':'What can’t talk but will reply when spoken to?','darkness':'The more of this there is, the less you see. What is it?','name':'It belongs to you, but other people use it more than you do','piano':'What has many keys but can’t open a single lock?'}
  ans, q = random.choice(list(riddle.items()))
  return(ans,q)

#function for jokes using jokes api
def joke():
  url = 'https://api.jokes.one/jod' # formats the api for jokes 
  response = requests.get(url)
  jokes=response.json()['contents']['jokes'][0]
  return(jokes['joke']['text'])

#function to print message when logged in
@client.event
async def on_ready():
  print("Ready to go")

next_ans=False #variable to check is next message will be a reply to riddle
tries=3 # counts number of tries for riddle
a='' #stores answer of riddle
game=False #to check if game is running
x=0 # stores the random number for the game
g_tries=5 #stores tries for game
news=False #tells whether the next input is for news
#function to react to a message
@client.event
async def on_message(message):
  global next_ans
  global tries
  global a
  global game
  global x
  global g_tries
  global news
  if message.author==client.user:# checks if sender is bot itself
    return
  
  elif next_ans==True: # checks for riddle answer
    if a in message.content.lower():
      await message.channel.send("Correct! Well done.")
      next_ans=False
      tries=3
    else:
      tries-=1
      if tries>0:
        await message.channel.send("Its ok try again, you still have {} tries".format(tries))
        return
      else:
        await message.channel.send("The correct answer is: {}".format(a))
        next_ans=False
  
  elif game==True:# checks is the game is being played
    if x in message.content:
      await message.channel.send("Correct! Well done.")
      game=False
      g_tries=5
    else:
      try:
        if int(message.content)>int(x):
          await message.channel.send("You guessed higher")
        else:
          await message.channel.send("You guessed lower")
        g_tries-=1
        if g_tries>0:
          await message.channel.send("Its ok try again, you still have {} tries".format(g_tries))
          return
        else:
          await message.channel.send("The correct answer is: {}".format(x))
          game=False
          g_tries=5
      except:# makes sure input is int
        await message.channel.send("Please enter only numbers")
    
  elif message.content.lower().startswith("hello") or message.content.lower().startswith('hi'):# introductory response
    await message.channel.send("Hello! {}".format(message.author))
    await message.channel.send("I am 3E, I stand for Educate Entertain and Encourage\nDepending on your mood I can perform these for you, so what do you want to do today?")
  
  elif 'bye' in message.content.lower():# sends goodbye message
    await message.channel.send("See you later!")
  
  elif 'educate' in message.content.lower():# checks for relax input
    await message.channel.send("Which category are you interested in?\n1.Business\n2.Entertainment\n3.General\n4.Health\n5.Science\n6.Technology\n")
    news=True
  
  elif 'entertain' in message.content.lower():# checks for entertain input
    await message.channel.send("Cool. Do you want to listen to music, play a game, hear a joke or solve a riddle? ")
  
  elif 'encourage' in message.content.lower():# checks for encourage input
    await message.channel.send("Hey cheer up! Let me tell you a nice quote to get you started..")
    await message.channel.send(motivate())
    time.sleep(3)
    await message.channel.send("Now its time to meditate for 1 min, breathe in and out along with me..")
    # loop for guided meditation
    t=0
    while(t<60):
      await message.channel.send("Breathe in")
      time.sleep(5)
      await message.channel.send("Hold")
      time.sleep(5)
      await message.channel.send("Breathe out")
      time.sleep(5)
      await message.channel.send("Hold")
      time.sleep(5)
      t+=20
    await message.channel.send("Done! Hope you are feeling relaxed now.")
    
  
  elif 'joke' in message.content.lower():# check if you want to listen to a joke
    await message.channel.send("Joke of the day:")
    await message.channel.send(joke())
  
  elif 'game' in message.content.lower():# checks for game input
    game=True
    await message.channel.send("You will get 5 turns to guess a number between 0 and 100")
    x=str(random.randint(0,100))
  
  elif 'riddle' in message.content.lower():#checks for riddle input
    a,q=riddles()
    await message.channel.send(q)
    next_ans=True

  elif news:
    await message.channel.send(get_news(message.content))
    news=False

  # sends playlist of top 50 of week 
  elif 'song' in message.content.lower() or 'music' in message.content.lower():
    await message.channel.send("https://www.youtube.com/playlist?list=PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG")
  
  
  
#to run the bot
keep_alive()
client.run(token)
    

  
