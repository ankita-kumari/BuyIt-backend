#!flask/bin/python
from flask import abort, request, Flask, jsonify
import sys
import bs4
import urllib2
import urllib
import operator

print(sys.real_prefix)
app = Flask(__name__)

@app.route('/')
def get_item():
	# task = [task for task in tasks if task['id'] == task_id]
	# if len(task) == 0:
	# 	abort(404)
	# return jsonify({'task': task[0]})
	url = getCheapest(request.query_string)
	return jsonify({'url': url})
	# return "Hello, World!"

def getCheapest( query ):
	query = urllib.urlencode ( { 'q' : query } )

	link = 'http://www.mysmartprice.com/msp/search/search.php?' + query
	headers = { 'User-Agent' : 'Mozilla/5.0' }
	request = urllib2.Request(link, headers=headers)

	response = urllib2.urlopen ( request ).read()
	response = response.replace('</html>', '', 1)

	soup = bs4.BeautifulSoup( response )
	text = soup.prettify()

	products = dict()
	for product in soup.find_all("div", class_="msplistitem"):
		price = product.find_all('span', class_='item-price')
		price = price[0].find_all('span', class_='price-val')
		price = price[0].get_text()
		str = "Rs. "
		if not (str in price):
			continue
		price = price[3:]
		price = price.replace(',', '')
#		title = item.find_all('a', class_='item-title')
#       title = title[0].get_text()

		href = product.find_all('a', class_='imgcont')
		href = href[0].get('href')
		products[href] = price
	sorted_items = sorted(products.items(), key=operator.itemgetter(1))
	return sorted_items[0][0]

if __name__ == '__main__':
	app.run(debug=True)
