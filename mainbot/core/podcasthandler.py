import feedparser as fp 
import requests
import json
from math import ceil

def Pagination(totlen:int,indsiz:int):
    return ceil(totlen/indsiz)


def PodSearch(query):
    formattedQuery = query.replace(' ', '+')
    response = requests.get(f"https://itunes.apple.com/search?term={formattedQuery}&entity=podcast").json()
    try:
        Result = response['results'][0]
        stuff_to_return = {
            "name":Result['collectionName'],
            "rss":Result['feedUrl'],
            "image":Result['artworkUrl100'],
            "count":Result['trackCount'],
            "date":Result['releaseDate'][:-10]
        }
    except IndexError:
        stuff_to_return = {
            "name": "Podcast Not Found",
            "rss": ' ',
            "image": ' ',
            "count": ' ',
            "date": ' This date is in Future wut '
        }
    return stuff_to_return

def RawSearch(query):
    formattedQuery = query.replace(' ', '+')
    response = requests.get(f"https://itunes.apple.com/search?term={formattedQuery}&entity=podcast").json()
    Result = response['results']
    return Result    

def PodResults(query):
    formattedQuery = query.replace(' ', '+')
    response = requests.get(f"https://itunes.apple.com/search?term={formattedQuery}&entity=podcast").json()
    Results = response['results']
    return Results


class Podcast:
    entries = {}
    def __init__(self,name,rsslink):
        self.name = name
        self.rsslink = rsslink
        self.feed = fp.parse(rsslink)
        self.entries = self.feed.entries
        

    def ListEpisodes(self):
        returnarr = []
        for entry in self.entries:
            returnarr.append(entry.title)
        return returnarr
    
    def GetEpisodeMp3(self,arg=0):
        if(type(arg) == int):
            return self.__Mp3Scrape__(self.entries[arg])
        elif(type(arg) == str):
            for entry in self.entries:
                if(arg in entry):
                    return self.__Mp3Scrape__(arg)
            
        
    def __Mp3Scrape__(self,entry):
        link = entry['links'][0]['href'] 
        if('.mp3' not in link):
            link = entry['links'][1]['href']
        return link
    
    def PodcastImage(self,arg = 0):
        arg = 0
        entry = self.entries[arg]
        try:
            return entry['image']['href']
        except:
            try:
                return self.feed['feed']['image']['href']
            except:
                pass
    
    def GetFeedDetails(self):
        xfeed = self.feed['feed']
        details = {
            'name':xfeed['title'],
            'link':xfeed['link'],
            'image':xfeed['image'],
            'author':xfeed['author'],
            'summary':xfeed['summary']
        }
        return details
    
    def GetEpisodeDetails(self,epno):
        entry = self.entries[epno]
        try:
            details = {
                'title':entry['title'],
                'summary':entry['summary'],
                'link':entry['link'],
                'published':entry['published']
            }
        except:
            details = {
                'title':entry['title'],
                'summary':entry['summary'],
                'link':'https://feeds.megaphone.fm/',
                'published':' '
            }
        return details
    



 
