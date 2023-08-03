import requests

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

add_user_to_server('MTEzNTE5OTAwOTc3MDg1MjM4Mg.GuSPD2.PK7c5jguu4_Aq9zG695cvyzH5biNPNbQqnH2dY', '1134274007848468561', '1136591869007122515', 'plCpYzvr2ZRWMq984WcdBNBDY5hDvU')