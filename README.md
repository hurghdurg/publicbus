# publicbus
Website showing where buses are in the Romanian county of Prahova using CJPH's (private?) API used in their app.
I'm not particularly experienced with JavaScript, so the code might be jank there.
BOTH the web server and the python file need to be running on the same host to work with the instructions i gave!
I looked at the TJP app's terms of conditions and I dont think I saw a line telling me I can or can't do this.
Also they seem to have a website that shows the bus routes... but I dont know if it also shows where they are on the map.. oh well!

Requirements:
```
python3 (and python3-fastapi, python3-requests, python3-dotenv, uvicorn)
nginx (or whichever webserver you prefer that can reverse proxy)
```

Debian requirements one-liner: ``apt install python3 python3-fastapi python3-requests python3-dotenv uvicorn nginx``

Instructions:
1. install all requirements on your host machine/server
2. clone the repo to your nginx webserver root
3. add a .env file defining the email and password of an active TJP account
example:
```
file: ./.env
email=example@example.org
password=password123!
```
4. change your nginx config (or steal mine "nginx-conf.example") (/etc/nginx/sites-enabled/default --- check if its different on your os!) and add the following:
```
location /fetch {
  proxy_pass http://127.0.0.1:2477/fetch;
}
```
5. save and enable/start nginx
6. while in the root of the cloned repo, run the command ``uvicorn --host 127.0.0.1 --port 2477 fetch:app``
7. done!

tested on a machine running Debian 13
