# statman

just a small throw away project to monitor my headless AI computer on my local network.

## WARNING

DO NOT use this outside of your LAN or in any other network you don't fully trust.  
It has no security what soever and is not meant to be used directly connected to the Internet!

## setup / start

Access: http://localhost:7001

### Windows

````bat
start.bat
````

### Linux / Mac
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## TODO

The docker files do not work (surprise, surprise, since the program needs a lot of low level access to the system)
