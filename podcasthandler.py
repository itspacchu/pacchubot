import feedparser as fp 
import requests
import json
from math import ceil

def Pagination(totlen:int,indsiz:int):
    return ceil(totlen/indsiz)

def EpisodeSearch(query,searchIndex):
    formattedQuery = query.replace(' ','+')
    response = requests.get(f"https://itunes.apple.com/search?term={formattedQuery}&entity=podcastEpisode").json()
    try:
        Result = response['results'][searchIndex]
        stuff_to_return = {
            "name":Result['artistIds'][0]['collectionName'],
            "rss":Result['episodeUrl'],
            "image":Result['artworkUrl160'],
            "count":0,
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

def PodSearch(query,searchIndex=0):
    formattedQuery = query.replace(' ', '+')
    response = requests.get(f"https://itunes.apple.com/search?term={formattedQuery}&entity=podcast").json()
    try:
        Result = response['results'][searchIndex]
        return Podcast(Result['collectionName'],Result['feedUrl'],Result['collectionId'])
    except IndexError:
        stuff_to_return = None


def RawSearch(query):
    formattedQuery = query.replace(' ', '+')
    response = requests.get(f"https://itunes.apple.com/search?term={formattedQuery}&entity=podcast&limit=5").json()
    Result = response['results']
    return Result  

def RawEpisodeSearch(query):
    formattedQuery = query.replace(' ', '+')
    response = requests.get(f"https://itunes.apple.com/search?term={formattedQuery}&media=podcast&entity=podcastEpisode&limit=5").json()
    Result = response['results']
    return Result   

def PodResults(query):
    formattedQuery = query.replace(' ', '+')
    response = requests.get(f"https://itunes.apple.com/search?term={formattedQuery}&entity=podcast").json()
    Results = response['results']
    return Results

class PodcastEpisode:
    def __init__(self,query,searchIndex=0):
        self.result = self.RawEpisodeSearch(query)[searchIndex]
        self.name = self.result['collectionName']
        self.podcast = self.GetPodcast()
    
    def GetEpisodeTitle(self):
        try:
            return self.result['trackName']
        except KeyError:
            return self.result['collectionName']

    def GetEpisodeAuthor(self):
        try:
            return self.result['artistName']
        except:
            return "Unknown"

    def GetEpisodeDuration(self):
        return self.result['trackTimeMillis']/1000

    def GetEpisodeMp3(self):
        return self.result['episodeUrl']
    
    def GetEpisodeImage(self):
        try:
            return self.result['artworkUrl160']
        except KeyError:
            return self.result['artworkUrl600']
    
    def GetEpisodeDescription(self):
        return self.result['description'].replace('<br>','\n')[:200]

    def GetPodcast(self): 
        return PodSearch(self.name)

    def GetItunes(self):
        return self.result['collectionViewUrl']

    def RawEpisodeSearch(self,query):
        formattedQuery = query.replace(' ', '+')
        response = requests.get(f"https://itunes.apple.com/search?term={formattedQuery}&media=podcast&entity=podcastEpisode&limit=5").json()
        Result = response['results']
        return Result   



class Podcast:
    entries = {}
    def __init__(self,name,rsslink,id):
        self.name = name
        self.rsslink = rsslink
        self.feed = fp.parse(rsslink)
        self.entries = self.feed.entries
        self.id = id
        self.author = self.feed['feed']['author']
 

    def ListEpisodes(self):
        returnarr = []
        for entry in self.entries:
            returnarr.append(entry.title)
        return returnarr
    
    def searchEpisode(self,query):
        for entry in self.entries:
            if(query in entry):
                return entry

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
            'summary':xfeed['summary'],
            'content':xfeed['content'],
            'tags':[i['term'] for i in xfeed['tags']]
        }
        return details
    
    def GetEpisodeDetails(self,epno):
        entry = self.entries[epno]
        try:
            details = {
                'title':entry['title'],
                'summary':entry['summary'],
                'link':entry['links'][0]['href'],
                'published':entry['published'],
                'duration':int(entry['itunes_duration'],10)/60,
                'image':entry['image']['href'],
                'author':entry['author']
            }
        except:
            details = {
                'title':entry['title'],
                'summary':entry['summary'],
                'link':'https://feeds.megaphone.fm/',
                'published':' '
            }
        return details