import requests
import get_info
import discord
from discord import app_commands
import time
import asyncio

def get_config():
    import json
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    return data   



def get_recent(pid):

    rq = requests.get(f"https://scoresaber.com/api/player/{pid}/scores?limit=1&sort=recent&page=1")
    rq = rq.json()
    stripped = {
        "songname": rq["playerScores"][0]["leaderboard"]["songName"] + " " + rq["playerScores"][0]["leaderboard"]["songSubName"],
        "diff": rq["playerScores"][0]["leaderboard"]["difficulty"]["difficultyRaw"].split("_"),
        "PP": rq["playerScores"][0]["score"]["pp"],
        "maxscore": rq["playerScores"][0]["leaderboard"]["maxScore"],
        "score": rq["playerScores"][0]["score"]["baseScore"],
        "acc": rq["playerScores"][0]["score"]["baseScore"] / rq["playerScores"][0]["leaderboard"]["maxScore"],
        "lb_pos": rq["playerScores"][0]["score"]["rank"]
    }
    #print(stripped.get("songname"))

    for i in stripped:
        print(stripped.get(i))

    #print(stripped.get("songname") + " " + stripped.get("songsub"))



    #print(score)
    # 2657138211032529

