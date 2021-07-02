from .__imports__ import *

# The full path to the repository root.
PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_PACKAGE.joinpath('.env'))
print(PROJECT_PACKAGE)
def env_to_bool(env, default):
    str_val = os.environ.get(env)
    return default if str_val is None else str_val == 'True'

# file imports
# db init
mongo_url = f"mongodb+srv://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{os.environ['MONGO_INITDB_ROOT_PASSWORD']}@{os.environ['MONGO_HOST']}"
mongo_client = MongoClient(mongo_url)

# global variables
version = "v1.7.3 beta"
http = urllib3.PoolManager()
ani = Jikan()
self_name = "Pacchu's Bot"
self_avatar = "https://raw.githubusercontent.com/itspacchu/Pacchu-s-Slave/master/Screenshot%202021-04-09%20225421.png"
command_prefix = "p."
command_prefix_use = ['_', 'p.', 'pacchubot.']

guild_ids = [685469328929587268, 705682250460823602, 737504783937830924]


ffmpeg_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel quiet'

ytdl_format_options = {
    'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
}

__all__ = [
    'version',
    'http',
    'ani',
    'self_name',
    'self_avatar',
    'command_prefix',
    'guild_ids',
    'mongo_client',
    'ytdl_format_options',
    'ffmpeg_options',
]
