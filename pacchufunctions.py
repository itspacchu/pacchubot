
def __initiate_default_stats__(serverlist:dict,serverid:str):
    serverlist[serverid] = {
        'emoji':'🌊',
        'debug':0,
        'bruh':'https://media.discordapp.net/attachments/760741167876538419/760744075132534784/DeepFryer_20200930_113458.jpg?width=448&height=518',
        'prefix' : '',
        'stats': {
            'bot_summons':0,
            'ecchi_command':0,
            'hugs':0,
            'pats':0,
            'kiss':0,
            'kills':0,
            'anipics':0,
            'anime':0,
            'manga':0,
            'echos':0,
            'bruhs':0,
            'nice':0
        }
        }

def __count_statistics__(serverlist:dict,serverid:str,stattitle:str):
    try:
        serverlist[serverid]['stats'][stattitle] += 1
    except KeyError:
        __initiate_default_stats__(serverlist,serverid)

def mentionToId(mention:str):
    return int(mention[3:-1])

def queryToName(var):
    name = ""
    for _ in var:
        name += " " + _
    return name

def list_to_string(the_list,no_of_items:int):
    returnstr = ''
    count = 0
    for _ in the_list:
        if(count > no_of_items):
            break
        count+= 1
        returnstr += str(_ + "\n")
    return returnstr