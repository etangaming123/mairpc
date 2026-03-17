import flask
from pypresence import Presence
import json
import os

if not os.path.exists("env.json"):
    with open("env.json", "w") as f:
        json.dump({
            "token": "YOUR_DISCORD_BOT_TOKEN_HERE",
            "user_id": 123456789012345678,
            "channel_id": 123456789012345678,
            "maimaiusername": ""
        })
    input("Please set up your env.json file with your bot token, user ID, and channel ID.")
    exit()

with open("env.json", "r") as f:
    env = json.load(f)

presenceclient = Presence(client_id=1437014727241895976)
youruserid = env["user_id"]

app = flask.Flask(__name__)
@app.route('/start_rpc', methods=['POST'])
def start_rpc():
    data = flask.request.json
    if data['user_id'] != youruserid:
        return {"error": "You are not authorized to use this command."}, 403
    presenceclient.connect()
    presenceclient.update(details="In queue // waiting for washing machine", state=f"{env['maimaiusername']} // Rating: {data['rating']}", start=data['ctime'], large_image="maimai", large_text="maimai RPC by etan", small_image="pfpicon", small_text=f"playing as {env['maimaiusername']}", buttons=[{"label": "source code", "url": "https://github.com/etangaming123/mairpc"}])
    return {"message": "Welcome to maimai!"}, 200

@app.route('/inqueue', methods=['POST'])
def inqueue():
    data = flask.request.json
    
    if data['user_id'] != youruserid:
        return {"error": "You are not authorized to use this command."}, 403
    global ctime
    ctime = data['ctime']
    global playing
    playing = False
    presenceclient.update(details="In queue // waiting for washing machine", state=f"{env['maimaiusername']} // Rating: {data['rating']}", start=data['ctime'], large_image="maimai", large_text="maimai RPC by etan", small_image="pfpicon", small_text=f"playing as {env['maimaiusername']}", buttons=[{"label": "source code", "url": "https://github.com/etangaming123/mairpc"}])
    return {"message": "Status set to in queue."}, 200

@app.route('/playing', methods=['POST'])
def playing():
    data = flask.request.json
    
    if data['user_id'] != youruserid:
        return {"error": "You are not authorized to use this command."}, 403
    global playing
    if not playing:
        global ctime
        ctime = data['ctime']
        playing = True
    presenceclient.update(details=f"In game // tapping funny buttons", state=f"{env['maimaiusername']} // Rating: {data['rating']}", start=data['ctime'], large_image="maimai", large_text="maimai RPC by etan", small_image="pfpicon", small_text=f"playing as {env['maimaiusername']}", buttons=[{"label": "source code", "url": "https://github.com/etangaming123/mairpc"}])
    return {"message": "Status set to playing maimai."}, 200

@app.route('/stop_rpc', methods=['POST'])
def stop_rpc():
    data = flask.request.json
    
    if data['user_id'] != youruserid:
        return {"error": "You are not authorized to use this command."}, 403
    presenceclient.clear()
    presenceclient.close()
    return {"message": "RPC stopped."}, 200

if __name__ == '__main__':
    app.run(port=6767) # HAHAHAHHAHAHA IM SO FUNNY SIX SEVEEEENNNN