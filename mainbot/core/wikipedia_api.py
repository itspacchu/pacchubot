# some cool self made api stuff

import requests
import json
from datetime import datetime


SESSION = requests.Session()
ENDPOINT = "https://en.wikipedia.org/w/api.php"

def fetch_potd(cur_date):
	date_iso = cur_date.isoformat()
	title = "Template:POTD/" + date_iso[:10]

	params = {
	  "action": "query",
	  "format": "json",
	  "formatversion": "2",
	  "prop": "images",
	  "titles": title
	}

	response = SESSION.get(url = ENDPOINT, params = params)
	data = response.json()
	filename = data["query"]["pages"][0]["images"][0]["title"]
	image_page_url = "https://en.wikipedia.org/wiki/" + title
	
	image_data = {
	  "filename": filename,
	  "image_page_url": image_page_url,
	  "image_src": fetch_image_src(filename),
	  "date": date_iso
	}	
	return image_data

def fetch_image_src(filename):
	params = {
	  "action": "query",
	  "format": "json",
	  "prop": "imageinfo",
	  "iiprop": "url",
	  "titles": filename
	}	
	response = SESSION.get(url = ENDPOINT, params = params)
	data = response.json()
	page = next(iter(data["query"]["pages"].values()))
	image_info = page["imageinfo"][0]
	image_url = image_info["url"]	
	return image_url


