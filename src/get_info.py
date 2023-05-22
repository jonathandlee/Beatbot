import requests


def get_player(name):
    #print(requests.get(f"https://scoresaber.com/api/players?search={name}").json())
    try:
        uid = requests.get(f"https://scoresaber.com/api/players?search={name}").json()["players"][0]["id"]
    except:
        return "Error: player not found"

    return uid

def get_recent(pid):
    """Returns the json-encoded content of a response, if any.

            :param \*\*kwargs: Optional arguments that ``json.loads`` takes.
            :raises requests.exceptions.JSONDecodeError: If the response body does not
                contain valid json.
            """
    rq = requests.get(f"https://scoresaber.com/api/player/{pid}/scores?limit=1&sort=recent&page=1")
    user = requests.get(f"https://scoresaber.com/api/player/{pid}/basic").json()

    rq = rq.json()
    #print(rq)
    try:   
        b = rq["playerScores"][0]["leaderboard"]["songName"]
    except:
        return "Failure"

    stripped = {
        "songname": rq["playerScores"][0]["leaderboard"]["songName"] + " " + rq["playerScores"][0]["leaderboard"]["songSubName"],
        "diff": rq["playerScores"][0]["leaderboard"]["difficulty"]["difficultyRaw"].split("_")[1],
        "pp": round(rq["playerScores"][0]["score"]["pp"],2),
        "weighted_pp": round(rq["playerScores"][0]["score"]["pp"] * rq["playerScores"][0]["score"]["weight"],2),
        "maxscore": rq["playerScores"][0]["leaderboard"]["maxScore"],
        "score": rq["playerScores"][0]["score"]["baseScore"],
        "acc": str(round((rq["playerScores"][0]["score"]["baseScore"] / rq["playerScores"][0]["leaderboard"]["maxScore"]*100),2)) + "%",
        "lb_pos": rq["playerScores"][0]["score"]["rank"],
        "song_author": rq["playerScores"][0]["leaderboard"]["songAuthorName"],
        "map_author": rq["playerScores"][0]["leaderboard"]["levelAuthorName"],
        "misses": rq["playerScores"][0]["score"]["missedNotes"],
        "bad_cuts": rq["playerScores"][0]["score"]["badCuts"],
        "cover": rq["playerScores"][0]["leaderboard"]["coverImage"],
        "player_name": user["name"],
        "profile": user["profilePicture"],
        "player_pp": user["pp"],
        "country": user["country"]
    }
    #print(stripped.get("songname"))

    # for i in stripped:
    #     print(stripped.get(i))
    return stripped
    #print(stripped.get("songname") + " " + stripped.get("songsub"))



    #print(score)
    # 2657138211032529

