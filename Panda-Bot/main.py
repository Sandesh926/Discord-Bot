import os
import discord
import requests
import json
import random
from replit import db
#from keep_alive import keep_alive
from googleapiclient.discovery import build
from discord.ext import commands

client = discord.Client()



#@client.command(aliases=["show"])
#async def showpic(ctx, *, search):
 #   ran = random.randint(0, 9)
  #  resource = build("customsearch", "v1", developerKey=api_key).cse()
   # result = resource.list(q=f"{search}", cx='f3cda7ee82e90b5f3', searchType="image").execute()
    #url = result["items"][ran]["link"]
    #embed1 = discord.Embed(title=f"Here Your Image ({search.title()})")
    #embed1.set_image(url=url)
    #await ctx.send(embed=embed1)



# For sad Words
sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "jahu", "alchi",
    "quit", "hap", "chodini ho", "sakdina", "hep"
]
starter_encouragement = [
    "Cheer_Up Bro!", "Chill hana na Bro!",
    "Your are great person..Always be happy",
    "I always believe in u bro! U can do it"
]

# for bot calling
bot_call = [
    "panda", "Panda", "PAnda", "pAnda", "PAnda", "PANda", "PANDa", "paNda",
    "panDA", "panDa", "pandu", "hello panda", "hi panda",
    "hello panda", "Pandu", "PANDA"]
bot_reply = [
    'Hello! I m fine and i hope u are doing well too.',
    "Bhana Brother! k xa khabar kina yad gareko",
    "Hello, This is baby panda. Nice to meet u😊"
]

# bot info details
info_call = ["info panda", "p/panda","p/pandainfo", "p/info", "p/info panda", "p/info Panda"]

# Person call
sandesh_call = ["Sandesh", "sandesh", "SANDESH", "Sandu",
                "sandu", "SAndesh", "sAndesh", "SANdesh", "SanDESH", "sanDesh"]

sandesh_reply = ['<@584783912736129025> Master u have been called.',
                 '<@584783912736129025> Someone might be calling u!!', '<@584783912736129025> Sire, U have been called!!!']

# avash_call
avash_call = ["Avash"]

avash_reply = ['<@622306805724479540> Chor, U have been called!!', '<@622306805724479540>,Antarastiya dumba!!',
               '<@622306805724479540> hero!! Balen ko Symbol, Au tw chat ma!!', '<@622306805724479540> Chomu!! Kata harako👿']

# umesh_call
umesh_call = ['umesh', 'xerxes', 'Umesh', 'UMESH', 'Xerxes']

umesh_reply = ['<@570458140202500108> Shau bro!! Chat ma aau tw', '<@570458140202500108> bro!!Ghar ko bada kati ho!!',
               '<@570458140202500108> g mane Genius sathi!!!', '<@570458140202500108> Curly aau tw discord ma!!']

# sandeep call
sandeep_call = ['sandeep', 'Sandeep', 'kale', 'Kale', 'Kalu', 'kalu']

sandeep_reply = ['<@719042132601471067> kalu mero mayalu!!', '<@719042132601471067>Beja, beja khana aau tw chat ma',
                 '<@719042132601471067> g mane genius..Auu chado', '<@719042132601471067> Aa kanxa kata maryau']


#subash call
subash_call = ['Suash','suash']
subash_reply = ['<@606481117196845088> bate bro k ho kata harako!!','A <@606481117196845088> kanxa kati dauntles hanxau..chat ma aau tw!! ']




@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


# Sad Words Responding
if "responding" not in db.keys():
    db["responding"] = True


# Function of qutoes..importing quote from external website
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return (quote)


# Function for encouraging message
def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db['encouragements'] = encouragements

    else:
        db["encouragements"] = [encouraging_message]


# Function for deleting encouragement message
def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db['encouragements'] = encouragements


#using Custom api to search images
client = commands.Bot(command_prefix="p/")
api_key = 'AIzaSyBgpEo4jFtinrdnT1uLGMVPKXlXBPPjKCQ'

@client.command(aliases=["show"])
async def showpic(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(q=f"{search}", cx="f3cda7ee82e90b5f3", searchType="image").execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Here Your Image ({search.title()}) Feature made by BOR NATION on YT")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)


  

# For Message Respond
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    mssg = message.content

    if message.content.startswith('p/inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db['responding']:
        options = starter_encouragement
        if "encourgements" in db.keys():
            options = options + db["encouragements"]

        if any(word in mssg for word in sad_words):
            await message.channel.send(random.choice(options))

    if mssg.startswith("p/addq"):
        encouraging_message = mssg.split("p/addq ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if mssg.startswith('del'):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(mssg.split("del", 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if mssg.startswith('p/list'):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if mssg.startswith("p/respond"):
        value = mssg.split("p/respond ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

    if any(word in mssg for word in bot_call):
        await message.channel.send(random.choice(bot_reply))

  #Response to Info panda
    if any(word in mssg for word in info_call):
        embed=discord.Embed(title="Panda Commands", url="https://realdrewdata.medium.com/", description="Here are the list of commands: \n p/addq(add new inspiration) \n p/list (To see the added inspiration) \n del 0 or 1(delete the latest inspiration according to the index) \n p/respond false (This stops the response from sad words) \n p/respond true (This continue the response from sad words) \n type sad words \n Type ur's friends name to ping them!! \n Say hi to panda", color=0xFF5733)
        await message.channel.send(embed=embed)

    if any(word in mssg for word in sandesh_call):
        round(client.latency * 1000)
        await message.channel.send(random.choice(sandesh_reply))

    if message.content.startswith('bijay'):
        round(client.latency * 1000)
        await message.channel.send('<@563257720321474580> bro..Naya bot bhanaune hoiena')


      
    if message.content.startswith('sampanna'):
        round(client.latency * 1000)
        await message.channel.send('<@377033662895620099> React developer bro mero mssg pani react gardeu na!!')

    if any(word in mssg for word in umesh_call):
        round(client.latency * 1000)
        await message.channel.send(random.choice(umesh_reply))

  #This is the idea of project

    if any(word in mssg for word in sandeep_call):
        round(client.latency * 1000)
        await message.channel.send(random.choice(sandeep_reply))

    if message.content.startswith('shishir'):
        round(client.latency * 1000)
        await message.channel.send('<@493727461012406284>khambu bro..k ho kati gf lai matra herxau..hamro mssg pani hera na!!')

    if message.content.startswith('chor'):
        round(client.latency * 1000)
        await message.channel.send('<@622306805724479540> bhandari chor..Timlai bolaxa')

    if message.content.startswith('sudip'):
        round(client.latency * 1000)
        await message.channel.send('<@735068468730396712> Front end developer handsome bro..Please reply garnus na hamlai pani')

    if any(word in mssg for word in avash_call):
        round(client.latency * 1000)
        await message.channel.send(random.choice(avash_reply))
      
    if any(word in mssg for word in subash_call):
        await message.channel.send(random.choice(subash_reply))

  
      
    if message.content.startswith('nitesh'):
        round(client.latency * 1000)
        await message.channel.send("<@819950988571181067> Nitu turi auu tw!!")
    
    if message.content.startswith('amir'):
        round(client.latency * 1000)
        await message.channel.send("<@436168655529705493> Don kata haryau..Au valorent bata chat ma!!")

    


# info Messages

# This will continue to run bot in web server
#keep_alive()


my_secret = os.environ['Key']
client.run(my_secret)

