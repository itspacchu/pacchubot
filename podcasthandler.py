import feedparser as fp 


podcasts = {
    0 : {
        "name":"crimejunkie",
        "rss":"https://feeds.megaphone.fm/ADL9840290619",
        "image":"https://upload.wikimedia.org/wikipedia/commons/0/0b/Crime_Junkie_Logo.jpg"
    },
    
    1 : {
        "name":"darknetdiary",
        "rss": "https://feeds.megaphone.fm/darknetdiaries"
    },
    
    2 : {
        "name":"redhanded",
        "rss": "https://rss.acast.com/redhanded"
    },
    
    3 : {
        "name":"waveform",
        "rss": "http://feeds.feedburner.com/WaveformWithMkbhd"
    }
}

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
    
            
crimejunkie = Podcast(
    'crimejunkie', "https://feeds.megaphone.fm/ADL9840290619")
