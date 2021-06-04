# september-15
from mainbot.utils import hasNumbers
from bs4 import BeautifulSoup
import requests

fetch_url = "https://imagine.gsfc.nasa.gov/hst_bday/"
months_list = ["january",
               "february",
               "march",
               "april",
               "may",
               "june",
               "july",
               "august",
               "september",
               "october",
               "november",
               "december"
               ]


def get_birthday_image(month,date):
    make_url = fetch_url + f"{month}-{date}"
    req = requests.get(make_url)
    soup = BeautifulSoup(req.text,"html.parser")
    socialimg = soup.findAll("div", {"class": "addthis_inline_share_toolbox"})[0]['data-media']
    return {"image-url":socialimg,
            "hubble-url":make_url}
    
    



