import urllib
import json as m_json
import sys
import bs4
import urllib2

query = raw_input ()
query = urllib.urlencode ( { 'q' : query } )

link = 'http://www.flipkart.com/search?q=' + query + '&as=off&as-show=off&otracker=start'
response = urllib2.urlopen ( link ).read()

soup = bs4.BeautifulSoup( response )

text = soup.prettify()

file_ = open('Flipkart_data.txt', 'w')
file_.write( text.encode('utf-8') )
file_.close()
