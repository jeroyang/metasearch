#coding=utf-8
import webapp2
import cgi
from models import *
import random

import os
import jinja2

import sys
reload(sys)
sys.setdefaultencoding('utf8')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('q') != '':
            query = self.request.get('q').split(' ')
            results = []
            result_count = dict()
            for Search in [GoogleSearch, YahooSearch, BingSearch, BaiduSearch]:
                searcher = Search()
                try:
                    results.extend(searcher.search(query))
                    result_count[Search.__name__] = searcher.result_count
                except:
                    result_count[Search.__name__] = 0
            logo = {'Google': 'http://www.google.com/favicon.ico',
                    'Yahoo': 'http://www.yahoo.com/favicon.ico', 
                    'Bing': 'http://www.bing.com/favicon.ico',
                    'Baidu': 'http://www.baidu.com/favicon.ico' }
            results = [(l, t, d, e, logo[e]) for (l, t, d, e) in results]
            template_values = {'results': results,
                               'query': self.request.get('q'),
                               'STATIC_URL': '/static/',
                               'google_count': result_count['GoogleSearch'], 
                               'yahoo_count': result_count['YahooSearch'], 
                               'bing_count': result_count['BingSearch'],
                               'baidu_count': result_count['BaiduSearch']
                               }
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))
        else:
            template_values = {'STATIC_URL': '/static/'}
            template = jinja_environment.get_template('welcome.html')
            self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)