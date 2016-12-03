import urllib2, re, scraperwiki
from bs4 import BeautifulSoup as bsoup4

class_attr_regex = re.compile(r'\.(?P<class_attr>.*?){display:none}') # .g3Kd{display:none}
PROXY_LIST_URL = 'http://proxylist.hidemyass.com/'

handle_request = urllib2.Request(PROXY_LIST_URL)
handle_response = urllib2.urlopen(handle_request)

soup = bsoup4(handle_response.read(), "lxml")

proxy_table = soup.find('table', attrs={'class':'hma-table'})

data={}
for tr in proxy_table.tbody.find_all('tr'):
	classes_to_exclude = []
	ip_address_text = []
	td_list = tr.find_all('td')
	port = td_list[2].text.strip()
	country = td_list[3].text.strip()
	connection_type = td_list[6].text.strip()
	anon = td_list[7].text.strip()
	style_tag_list = td_list[1].style.text.strip().split('\n') # [u'.g3Kd{display:none}', u'.OlWn{display:inline}', u'.wgUC{display:none}', u'.YY3C{display:inline}']
	for class_attr in style_tag_list:
		class_attr_match = class_attr_regex.search(str(class_attr))
		if class_attr_match:
			classes_to_exclude.append(class_attr_match.group("class_attr")) # ['g3Kd','wgUC']

	td_list[1].style.extract()
	ip_address_span_list = td_list[1]
	# Get visible IP address text
	for item in ip_address_span_list.find_all(text=True)[1:]:
		if item.parent.get('style') == 'display:none':
			continue

		_class = item.parent.get('class') # _class = [u'g3Kd']
		if _class:
			if _class[0] in classes_to_exclude: # _class[0] = u'g3Kd'
				continue

		if item.strip():
			ip_address_text.append(item)

	ip_address = ''.join(ip_address_text)
	scraperwiki.sqlite.save(unique_keys=["IP_Address"], data={"IP_address": ip_address, "Port": port, "Country": country, "Type": connection_type, "Anon": anon})
  
