from .__imports__ import *
from pprint import pprint


# file imports
jsonfile = io.open("mainbot/perks.json", mode="r", encoding="utf-8")

# db init
# mongo_url = f"mongodb+srv://{env_var['MONGO_INITDB_ROOT_USERNAME']}:{env_var['MONGO_INITDB_ROOT_PASSWORD']}@{env_var['MONGO_HOST']}"
mongo_url = "mongodb+srv://pacchu:kiminonawa@pslave.da85h.mongodb.net/test"
mongo_client = MongoClient(mongo_url)

# global variables
version = "v0.5.2"
http = urllib3.PoolManager()
ani = Jikan()
self_name = "Pacchu's Slave"
self_avatar = "https://raw.githubusercontent.com/itspacchu/Pacchu-s-Slave/master/Screenshot%202021-04-09%20225421.png"
command_prefix = '.'

guild_ids = [685469328929587268,705682250460823602]

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ffmpeg_options = {'options': '-vn'}

__all__ = [
    'version',
    'http',
    'ani',
    'self_name',
    'self_avatar',
    'command_prefix',
    'jsonfile',
    'guild_ids',
    'mongo_client',
    'ytdl_format_options',
    'ffmpeg_options',
]
