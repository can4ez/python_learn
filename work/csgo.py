import requests
import valve.source.a2s 
from requests import get
from time import sleep
from random import randint

SERVER_ADDRESS = ('37.18.21.245', 27050)
SERVER_VER_FILE = 'server'
STEAM_VER_FILE = 'steam'

COMMAND_STOP = "https://cyber-server.ru/servers/section/action/id/35/action/stop"
COMMAND_UPDATE = "https://cyber-server.ru/servers/section/action/id/35/action/update"
COMMAND_START = "https://cyber-server.ru/servers/section/action/id/35/action/start" 

RESPONSE_OKAY = '{"s":"ok"}'

HEADERS = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://cyber-server.ru/servers/id/35',
    'Cookie': 'bsp_login=...; bsp_passwd=...; bsp_authkeycheck=392bfe20097ed53099f632bce2c8f495',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origi',
}

def get_server_ver(addr):
    with valve.source.a2s.ServerQuerier(addr) as server:  
        ver = False
        try:
            data = server.info()
            ver = data["version"]
        finally:
            return ver

def get_steam_ver(): 
    # https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/steam.inf
    ver = False
    try:
        ver = False
        data = get(r"https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/steam.inf").text.split()
        for a in data:
            # ServerVersion=
            if a[0:13] == 'PatchVersion=':
                ver = a[13::]
                break
    finally:
        return ver

in_progress_update = False

def send_command(url):
    print(f'Send cmd: "{url}"')
    response = requests.get(
        url ,
        params={  },
        headers= HEADERS,
    )
    
    return response.text


def process_update():
    global in_progress_update

    in_progress_update = True

    res = send_command(COMMAND_STOP)
    if res != RESPONSE_OKAY:
        print(f'[ERROR] Ошибка отключения сервера: {res=}')
        sleep(3600)
        in_progress_update = False
        return

    sleep(randint(5,25))

    res = send_command(COMMAND_UPDATE)
    if res != RESPONSE_OKAY:
        res = send_command(COMMAND_START) # TODO
        in_progress_update = False
        print(f'[ERROR] Ошибка обновления сервера, возможно он уже обновляется: {res=}')
        return

    sleep(randint(5,25))

    c = 0
    while c < 10:
        c += 1
        res = send_command(COMMAND_START)
        if res != RESPONSE_OKAY: 
            sleep(randint(5,25))
            continue
        return

    print(f'[ERROR] Ошибка при запуске обновленного сервера')

 
while True: 
    if in_progress_update == True:
        continue

    server_version = get_server_ver(SERVER_ADDRESS)
    steam_version = get_steam_ver()

    print(f'{server_version=}')
    print(f'{steam_version=}') 

    if server_version != False and steam_version != False and server_version != steam_version:
        process_update()

    print(f'Sleep: 3600sec.')

    sleep(3600)


