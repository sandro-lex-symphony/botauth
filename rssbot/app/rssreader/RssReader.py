import feedparser
import json

class RssReader():
    def __init__(self, file):
        self.setFile(file)
        self._state = []
        self.loadState()
        
    def setFile(self, file):
        self._file = file

    def loadState(self):
        with open(self._file) as json_file:
            data = json.load(json_file)
            self._state = data['rss']

    def saveState(self):
        out = {
            "rss": self._state
        }

        with open(self._file, 'w') as output_file:
            json.dump(out, output_file)

    def stateHasRssUrl(self, url):
        for item in self._state:
            if item['url'] == url:
                return True
        return False
    
    def stateHasRssName(self, name):
        for item in self._state:
            if item['name'] == name:
                return True
        return False
    
    def checkrss(self):
        feeds = {}
        for item in self._state:
            nf = feedparser.parse(item['url'])
            if nf.status != 200: 
                print("Error getting feed " + item['name'])
                break
            if item['updated'] == nf.updated:
                print("no News to read")
            else:
                print("XXX FOUND feed")
                feeds[item['name']] = [] 
                item['updated'] = nf.updated
                for entry in nf.entries:
                    if entry['id'] not in item['lastread']:
                        print("New item: " + entry['id'])
                        feed = {
                            'title': entry['title'],
                            'link': entry['link']
                        }
                        feeds[item['name']].append(feed)
                        item['lastread'].append(entry['id'])
                self.saveState()
        return feeds


    def get_list(self):
        ret = []
        for item in self._state:
            ret.append(item['name'])
        return ret

    def del_rss_item(self, name):
        for i in range(len(self._state)):
            if self._state[i]['name'] == name:
                print("going to del " + name + ' ' + str(i))
                del(self._state[i])
                self.saveState()
                return True
        return False

    def add_rss_item(self, name, url):
        print(name)
        print(url)
        if self.stateHasRssName(name) or self.stateHasRssUrl(url):
            print("Error Rss exists")
            return False
        nf = feedparser.parse(url)
        if nf.status != 200:
            print("Error loading feed " + nf.status)
            return False
        if len(nf.entries) < 1:
            print("Error no feed found for " + name)
            return False
        self._state.append({
            'name': name,
            'url': url,
            'updated': '',
            'lastread': []
        })
        self.saveState()
        return True





