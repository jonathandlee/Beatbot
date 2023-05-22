import requests

#print("hi")



def get_recent(pid):

    rq = requests.get(f"https://scoresaber.com/api/player/{pid}/scores?limit=1&sort=recent&page=1")
    rq = rq.json()
    stripped = {
        "songname": rq["playerScores"][0]["leaderboard"]["songName"],
        "PP": rq["playerScores"][0]["score"]["pp"],
        "maxscore": rq["playerScores"][0]["leaderboard"]["maxScore"],
        "score": rq["playerScores"][0]["score"]["baseScore"],
        "acc": rq["playerScores"][0]["score"]["baseScore"] / rq["playerScores"][0]["leaderboard"]["maxScore"],
        "lb_pos": rq["playerScores"][0]["score"]["rank"]
    }
    print((stripped.get("songname")))


    #print(score)
    # 2657138211032529

if __name__ == '__main__':
    get_recent(2657138211032529)
    print("hi")
