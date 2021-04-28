# IMPORTS
from time import *
from random import *
import time
import re
import subprocess
import discord
from discord.utils import get
import os
import json
import io
import urllib3
import asyncio
import youtube_dl
import pymongo
from pymongo import MongoClient
from jikanpy import Jikan
import numpy as np
from discord.ext import commands
from pacchufunctions import __initiate_default_stats__, mentionToId, queryToName, list_to_string
