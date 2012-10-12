#coding=utf-8
from urllib2 import Request, urlopen
from urllib import urlencode, unquote
from BeautifulSoup import BeautifulSoup
import re

class BaseSearch(object):
    def __init__(self):
        self.url = 'http://www.google.com/search'
        self.q_term = 'q'
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                        'referer': 'http://www.google.com/'}
        self.result_count = -1
    
    def query(self, query):
        req = Request('%s?%s' % (self.url, query), headers=self.headers)
        html = BeautifulSoup(urlopen(req).read())
        result_count = re.sub(r'.*?about <b>([\d,]+)</b>.*', r'\1', str(html.find('td', nowrap='nowrap', align='right')))
        if result_count != 'None':
            self.result_count = int(re.sub(r',', '', result_count))
        for result in [x for x in html('p') if x.a]:
            link = result.a['href'][7:]
            title = re.sub(r'<.*?>', '', str(result.a)) or 'Link'
            desc = re.sub(r'<.*?>', '', str(result.font).split('<br />')[0])
            if desc is not None and re.match(r'http', link):
                yield (link, title, desc, 'Google')
    
    def search(self, terms):
        query = urlencode({self.q_term :'+'.join(terms)})
        return self.query(query)


class GoogleSearch(BaseSearch):
    pass

class BingSearch(BaseSearch):
    def __init__(self):
        self.url = 'http://www.bing.com/search'
        self.q_term = 'q'
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                        'referer': 'http://www.bing.com/'}
        self.result_count = -1

    def query(self, query):
        req = Request('%s?%s&go=&qs=n&pq=computer+science&sc=7-13&sp=-1&sk=&qpvt=computer+science&rf=1' % (self.url, query), headers=self.headers)

        html = BeautifulSoup(urlopen(req).read())
        result_count = re.sub(r'.*?([\d,]+).*', r'\1', str(html.find('span', id='count')))
        if result_count != 'None':
            self.result_count = int(re.sub(r',', '', result_count))
        for result in [x.parent.parent for x in html('h3') if x.parent.name=='div']:
            link = result.a['href']
            title = re.sub(r'<.*?>', '', str(result.a))
            desc = re.sub(r'<.*?>', '', str(result('p')))
            yield (link, title, desc, 'Bing')
            
            
class YahooSearch(BaseSearch):
    def __init__(self):
        self.url = 'http://search.yahoo.com/search'
        self.q_term = 'p'
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                        'referer': 'http://search.yahoo.com/'}
        self.result_count = -1
        
    def query(self, query):
        req = Request('%s?%s&fr=yfp&rd=r3' % (self.url, query), headers=self.headers)

        html = BeautifulSoup(urlopen(req).read())

        result_count = re.sub(r'.*?([\d,]+).*', r'\1', str(html.find('span', id='resultCount')))
        if result_count != 'None':
            self.result_count = int(re.sub(r',', '', result_count))
        for result in [x for x in html('h3') if re.match(r'.*?class="yschttl', str(x.a))]:
            link = unquote(re.sub(r'.*?\*\*', '', str(result.a['href'])))
            title = re.sub(r'<.*?>', '', str(result.a)) or 'Link'
            desc = re.sub(r'.*?<div .*? class="abstr.*?>(.*?)</div>.*', r'\1', str(result.parent.parent))
            desc = re.sub(r'<.*?>', '', desc)
            if desc is not None:
                yield (link, title, desc, 'Yahoo')

class BaiduSearch(BaseSearch):
    def __init__(self):
        self.url = 'http://www.baidu.com/s'
        self.q_term = 'wd'
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        self.result_count = -1

    def query(self, query):
        req = Request('%s?ie=utf-8&bs=computer+science+pdf&f=8&rsv_bp=1&rsv_spt=3&%s' % (self.url, query), headers=self.headers)

        html = BeautifulSoup(urlopen(req).read())
        result_count = re.sub(r'.*?>.*?([\d,]+).*', r'\1', str(html.find('span', {'class': "nums"})))
        if result_count != 'None':
            self.result_count = int(re.sub(r',', '', result_count))
        for result in [x for x in html('table') if re.match(r'[^>]*class="result"', str(x))]:
            link = unquote(re.sub(r'.*?\*\*', '', str(result.a['href'])))
            title = re.sub(r'<.*?>', '', str(result.a)) or 'Link'
            desc = re.sub(r'<br />.*', '', str(result.find('font', size='-1')))
            desc = re.sub(r'<.*?>', '', desc)
            if desc is not None:
                yield (link, title, desc, 'Baidu')
