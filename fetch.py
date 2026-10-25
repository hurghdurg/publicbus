import requests, datetime, time, os, json, asyncio
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

load_dotenv()

email = os.getenv('email')
password = os.getenv('password')
passtoken = ''
passrefreshtoken = ''

def acquiretoken():
    global passtoken
    global passrefreshtoken
    headers = {'password': password, 'username': email}

    r = requests.get('https://public.cjph.ro/api/identity', headers=headers)

    passtoken=r.cookies['PassToken']
    passrefreshtoken=r.cookies['PassRefreshToken']
    print('PassToken: ' + passtoken[:10] + ' [ ... ]')
    print('PassRefreshToken: ' + passrefreshtoken[:10] + ' [ ... ]')

def testrefreshtoken():
    global passtoken
    global passrefreshtoken
    cookies = dict(PassToken=passtoken, PassRefreshToken=passrefreshtoken)

    r = requests.get('https://public.cjph.ro/api/identity/test', cookies=cookies)
    if r.status_code == 200:
        print("Token valid/logged in!")

    elif r.status_code == 401:
        print("Token not acquired/token expired!")
        print("Trying to refresh...")
        r = requests.patch('https://public.cjph.ro/api/identity/refresh', cookies=cookies)
        if r.status_code == 200:
            passtoken=r.cookies['PassToken']
            passrefreshtoken=r.cookies['PassRefreshToken']
            print('PassToken: ' + passtoken[:10] + ' [ ... ]')
            print('PassRefreshToken: ' + passrefreshtoken[:10] + ' [ ... ]')
        elif r.status_code == 400:
            print("? try restarting the script?")
        else:
            print("?? server down/blocked?")
    else:
        print("? server down/blocked?")
    
def gnpdata():
    global passtoken            # im not sure if i need these two here but ill keep them just in case
    global passrefreshtoken
    cookies = dict(PassToken=passtoken, PassRefreshToken=passrefreshtoken)
    r = requests.get('https://public.cjph.ro/api/statii/status/44.9360000000/26.0180000000/1', cookies=cookies)
    if r.status_code == 200:
        rawdata = r.json()
        
        processeddata = [
                     {
                            "traseu": item["traseu"],
                            "position": item["position"],
                            "numar": item["numar"],     # i dont like json or python for that matter
                            "id": item["id"]
                     }
                     for item in rawdata
                     ]
        print(json.dumps(processeddata, indent=4))
        return processeddata
    elif r.status_code == 401:
        print("Token not acquired/token expired")
        print("Running refresh function...")
        testrefreshtoken()
        return None
    else:
        print("server down or no cookies passed?")
        return None

async def refreshloop():
    while True:
        testrefreshtoken()
        await asyncio.sleep(15)

@asynccontextmanager
async def lifespan(app: FastAPI):
    acquiretoken()
    testrefreshtoken()
    
    task = asyncio.create_task(refreshloop())
    
    yield
    
    task.cancel()
    print("turning off...")

app = FastAPI(lifespan=lifespan)

@app.get("/fetch")
def deliverdata():
    data = gnpdata()
    if data is None:
        raise HTTPException(status_code=500, detail="data not here oops")
    return data

