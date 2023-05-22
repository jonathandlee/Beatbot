import requests
import discord
from discord import app_commands
from src import listener
from src import get_info
from src import json_integs
import time
import datetime
import asyncio
import websockets
import json







def create_embed(id):
    print(id)
    info = get_info.get_recent(id)
    if info == "Failure":
        return discord.Embed(title="Invalid User Id! Please re-register with a valid scoresaber id")
    print(info)

    
    songname = info.get("songname")
    diff = info.get("diff")
    pp = info.get("pp")
    w_pp = info.get("weighted_pp")
    ss = info.get("score")
    ms = info.get("maxscore")
    acc = info.get("acc")
    lb = info.get("lb_pos")
    sa = info.get("song_author")
    ma = info.get("map_author")
    miss = info.get("misses")
    bc = info.get("bad_cuts")
    player_pp = info.get("player_pp")
    pfp = info.get("profile")
    pname = info.get("player_name")
    country = info.get("country")
    cover = info.get("cover")

    embed = discord.Embed(title=sa + " - " + songname,
                      url="https://scoresaber.com/leaderboard/402110",
                      description= f"{diff} - Mapped by {ma}\n\nUser: **[{pname}](https://scoresaber.com/u/{id})** ({lb}th global)",
                      colour=0x00b0f4,
                      timestamp=datetime.datetime.now())
    embed.set_author(name=f"{pname} - {player_pp}pp - {country}")
    embed.add_field(name="Score",
                    value=f"{ss} out of {ms}",
                    inline=True)
    embed.add_field(name="PP (Weighted)",
                    value=w_pp,
                    inline=True)
    embed.add_field(name="PP (Unweighted)",
                    value=pp,
                    inline=True)
    embed.add_field(name="Misses",
                    value=miss,
                    inline=True)
    embed.add_field(name="Bad Cuts",
                    value=bc,
                    inline=True)
    embed.add_field(name="Accuracy",
                    value=acc,
                    inline=True)
    embed.set_thumbnail(url=cover)
    embed.set_footer(text="Issues? Message me at lobsterrrrrrrrrr#0884",
                    icon_url=pfp)
    return embed

async def handle_message(message,ctx: discord.Interaction):
        """Handles the message [message] in context [ctx]. Gets user id from [ctx], which is then turned into a scoresaber id."""
        uuid = str(get_user(ctx.user.id))
        # Process the WebSocket message and send a Discord message
        #await ctx.followup.send(f"Received a WebSocket update: {message}")
        try: 
            response = json.loads(message)
            uid = response["commandData"]["score"]["leaderboardPlayerInfo"]["id"]
            print(uid)
            if uid != uuid:
                #print("uh?")
                embed_to_end = create_embed(uid)
                await ctx.followup.send("",embed=embed_to_end)
        except:
            print("idek")
            #return 0



async def listen_to_websocket(ctx:discord.Interaction):
    websocket = await websockets.connect('wss://scoresaber.com/ws')  # Replace with your WebSocket URL
    while True:
        message = await websocket.recv()
        await handle_message(message,ctx)




async def handle_messages(message,ctx: discord.Client):
        """Handles the message [message] in context [ctx]. Gets user id from [ctx], which is then turned into a scoresaber id."""



        #uuid = str(get_user(ctx.user.id))
        # if score uid is in listen_users.keys():
        # for i in listen_users[uid]: await client.send



        # Process the WebSocket message and send a Discord message
        #await ctx.followup.send(f"Received a WebSocket update: {message}")
        try: 
            response = json.loads(message)
            uid = response["commandData"]["score"]["leaderboardPlayerInfo"]["id"]

            print("first try entrance")

            print(uid)
            keys = json_integs.get_keys()
            print(keys)
            print(uid not in keys)
            

            if str(uid) in keys:
                embed_to_end = create_embed(uid)
                channels = json_integs.get_listeners(uid)
                print("getting channels")
                print(channels)
                for i in channels:
                    channel = ctx.get_channel(i)
                    print("attempting to send")
                    await channel.send("",embed=embed_to_end)
                

                #print("uh?")
                #embed_to_end = create_embed(uid)
                #channel = ctx.get_channel()

                #await ctx.followup.send("",embed=embed_to_end)
        except:
            print("idek")
            #return 0

async def listen_to_websocket_messages(ctx: discord.Client):
    websocket = await websockets.connect('wss://scoresaber.com/ws')  # Replace with your WebSocket URL
    while True:
        message = await websocket.recv()
        await handle_messages(message, ctx)


def get_config():
    """OPens the config file associated with the bot; should contain your auth token for discord, as well as any additional authentication tokens"""
    import json
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    return data   

def get_user(id):
    """Gets the scoresaber id associated with discord user [id]"""
    import json
    with open("users.json", "r") as jsonfile:
        data = json.load(jsonfile)
        #print(type(data))
    #print(data)
    #print(data[str(id)])
    return data[str(id)]


def update_users(disc_id,ss_id):
    with open('users.json', 'r') as file:
        data = json.load(file)
    print(data)
    data[disc_id] = ss_id 
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4) 
    



config = get_config()

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents().default())
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.streaming, name="/recent")

def initialize_bot():
    """Initialize PyGPT Bot Client"""
    client = aclient()

    

    @client.event
    async def on_ready():
        await client.tree.sync()
        await listen_to_websocket_messages(client)

    @client.tree.command(name="register",description="[Required for bot usage] register your profile with the bot!")
    async def register(interaction: discord.Interaction, *, scoresaber_id: str):
        await interaction.response.defer(ephemeral=False)
        discord_id = interaction.user.id
        scoresaber_id = int(scoresaber_id)
        update_users(discord_id, scoresaber_id)
        json_integs.add_listeners(scoresaber_id)
        await interaction.followup.send(f"(Hopefully) successfully register discord id {discord_id} with scoresaber id {scoresaber_id}")

        

    @client.tree.command(name="recent",description="Get your most recent score!")
    async def recent(interaction: discord.Interaction):
        print(interaction.user.id)

        await interaction.response.defer(ephemeral=False)
        scoresaber_id = get_user(interaction.user.id)


        embed_to_end = create_embed(scoresaber_id)

        await interaction.followup.send(f"Howdy, {interaction.user.name}",embed=embed_to_end)

    @client.tree.command(name="recentname",description="Get a user id's most recent score!")
    async def recentname(interaction: discord.Interaction, *, name: str):
        await interaction.response.defer(ephemeral=False)
        uid = get_info.get_player(name)

        if uid == "Error: player not found":
            await interaction.followup.send("Could not find this user; please try again")
        else:
            #scoresaber_id = get_user(interaction.user.id)


            embed_to_end = create_embed(uid)

            await interaction.followup.send(f"Howdy, {interaction.user.name}",embed=embed_to_end)

    # WebSocket setup
    

    # Start the bot and WebSocket listener


    @client.tree.command(name="listen",description="Listen to the scores feed for recent scores!")
    async def listen(interaction: discord.Interaction):
        print(interaction.user.id)
        
        
        await interaction.response.defer(ephemeral=False)
        ssid = get_user(interaction.user.id)


        #await interaction.followup.send(f"Waiting for plays from {interaction.user.name}")
        json_integs.update_listeners(ssid,interaction.channel_id)
        await interaction.followup.send(f"Now waiting for plays from {interaction.user.name} in {interaction.guild_id}")




        #await listen_to_websocket(interaction)




        #await interaction.followup.send(f"Howdy, {interaction.user.name}",embed=embed_to_end)






    # Run client command response (Requires token to execute)
    client.run(config['discord_bot_token'])




    #print(stripped.get("songname") + " " + stripped.get("songsub"))



    #print(score)
    # 2657138211032529

