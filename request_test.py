import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
page = requests.get('http://www.bricklink.com/catalogPG.asp?S=21303-1', headers=headers)
source = page.text
soup = BeautifulSoup(source, 'lxml')
# name = soup.find('span', id='item-name-title').get_text()
table = soup.findAll('table')[12]
rows = table.findAll('td')
avg_price = rows[7].get_text()
# print name
print avg_price