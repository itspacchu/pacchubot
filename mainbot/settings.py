from .__imports__ import *

# The full path to the repository root.
PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_PACKAGE.joinpath('.env'))
print(PROJECT_PACKAGE)


def env_to_bool(env, default):
    str_val = os.environ.get(env)
    return default if str_val is None else str_val == 'True'

# db init
mongo_url = f"{os.environ['MONGO_KEY']}"
mongo_client = MongoClient(mongo_url)

# global variables
version = "v3 beta"
http = urllib3.PoolManager()
ani = Jikan()
self_name = "Pacchu's Bot"
self_avatar = "https://raw.githubusercontent.com/itspacchu/Pacchu-s-Slave/master/Screenshot%202021-04-09%20225421.png"
command_prefix = "p."
command_prefix_use = ['p.', '_']

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
