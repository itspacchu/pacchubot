# IMPORTS
import re
import requests
import json
import io
import urllib3
import youtube_dl
import discord
import asyncio
from random import choice
import feedparser as fp
import podcasthandler as ph
import gpt2api as g2a
import time as ttime
from discord.utils import get
from injectPayload import cartoonize
from pymongo import MongoClient
from jikanpy import Jikan
from discord.ext import commands
from pacchufunctions import __initiate_default_stats__, mentionToId, queryToName, list_to_string

# import subprocess
# import time
# import os
# import pymongo
# from discord import Spotify
# from discord_slash import SlashCommand, SlashContext
# import numpy as np
# from time import *