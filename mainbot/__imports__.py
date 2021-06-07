# IMPORTS
from abc import ABC
import psutil
import re
import os
import requests
import json
import io
import urllib3
import youtube_dl
import discord
import asyncio
from random import choice
from pathlib import Path
import feedparser as fp
from .core import g2a, cartoonize, ph,wikipedia_api
import time as ttime
from discord.utils import get
from inspect import getmembers
from dotenv import load_dotenv
from bson.objectid import ObjectId
from pymongo import MongoClient
from jikanpy import Jikan
import datetime
from discord.ext import commands
from discord.ext.commands import CommandError , CommandNotFound
from discord_components import DiscordComponents, Button , ButtonStyle,component,InteractionType
from .utils import *

# import subprocess
# import time
# import pymongo
# from discord import Spotify
# from discord_slash import SlashCommand, SlashContext
# import numpy as np
# from time import *
