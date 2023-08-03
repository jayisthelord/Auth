from flask import Flask, request
import requests
import json
import pymongo
from pymongo import MongoClient

uri = "mongodb+srv://jay:9U4USnSVyHTIzkB2@cluster0.pyypy0w.mongodb.net/?retryWrites=true&w=majority"
app = Flask(__name__)
client = MongoClient("mongodb+srv://jay:9U4USnSVyHTIzkB2@cluster0.pyypy0w.mongodb.net/?retryWrites=true&w=majority")
db = client['DLL']
collection = db['oauth2']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def add_user_to_server(token: str, user_id: str, server_id: str, access_token: str) -> bool:
    url = f'https://discordapp.com/api/v8/guilds/{server_id}/members/{user_id}'
    headers = {
        'Authorization': f'Bot {token}'
    }

    data = {
        "access_token": access_token
    }

    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f'User {user_id} added to server with ID {server_id}')
        return True
    else:
        print(f'Error adding user {user_id} to server with ID {server_id}')

@app.route('/auth/callback')
def callback():
    code = request.args.get('code')

    url = 'https://discord.com/api/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': '1135199009770852382',
        'client_secret': 'WgbhAm_cdeAqmwkm7KRXSyIOZsHxsUZH',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:5000/auth/callback',
        'scope': 'identify guilds.join'
    }
    response = requests.post(url, headers=headers, data=data).json()
    access_token = response['access_token']

    url = 'https://discord.com/api/users/@me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers).json()
    user_id = response['id']

    print(response)

    invite_code = '1136591869007122515'
    bot_token = 'token'
    add_user_to_server(bot_token, user_id, invite_code, access_token)

    psto = {user_id: {
        'AuthToken': access_token
    }}

    collection.insert_one(psto)

    return 'Successfuly authorised with Discord, you may now close this window.'

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)