from bs4 import BeautifulSoup
from selenium import webdriver
from collections import namedtuple
import sqlite3
import sys
import requests


Lego_Set = namedtuple('Lego_Set', ['times_sold', 'total_qty', 'min_price', 'avg_price', 'qty_avg_price', 'max_price'])

#creates the Lego_Set named tuple from row data
def getSetData(table):
	rows = table.find_all('td')

	clean_rows = []
	for row in rows:
		clean_rows.append(row.get_text())
	return Lego_Set(
		int(clean_rows[1]), 
		int(clean_rows[3]), 
		float(clean_rows[5][4:]), 
		float(clean_rows[7][4:]),
		float(clean_rows[9][4:]),
		float(clean_rows[11][4:])
	)

def addSet():
	lego_id = int(input("Enter Product ID: "))
	purchase_price = float(input("Enter Purchase Price: "))
	actual_selling_price = float(input("Enter sale price, 0 if not sold: "))
	shipping_cost = float(input("Enter shipping cost: "))
	estimated_selling_price = checkPrice(lego_id)
	conn = sqlite3.connect('lms.db')
	c = conn.cursor()
	sql_insert_set = """ INSERT INTO collection VALUES (?,?,?,?,?,?); """
	c.execute(sql_insert_set, (lego_id, 
								'placeholder name',
							 	purchase_price,
							 	estimated_selling_price,
							 	actual_selling_price,
							 	shipping_cost)
			)
	conn.commit()
	conn.close()
	return

def checkPrice(lego_id=-1):
	if (lego_id == -1):
		lego_id = int(input("Enter Product ID: "))
	url = 'http://www.bricklink.com/v2/catalog/catalogitem.page?S='+str(lego_id)+'#T=P'
	
	headers = {'User-Agent': "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
	page = requests.get('http://www.bricklink.com/catalogPG.asp?S=21303-1', headers=headers)
	source = page.text
	soup = BeautifulSoup(source, 'lxml')
	# name = soup.find('span', id='item-name-title').get_text()
	table = soup.findAll('table')[12]
	rows = table.findAll('td')
	avg_price = rows[7].get_text()
	# print name

	return avg_price


def main():
	num_args = len(sys.argv) - 1
	args = sys.argv[1:]
	if (num_args == 0):
		print 'No arguments given'
		return
	elif (num_args == 1):

		if (args[0] == 'add'):
			addSet()
		elif (args[0] == 'check'):
			print checkPrice()
		else:
			return
	else:
		return

if __name__ == '__main__':
	main()

# conn = sqlite3.connect('lms.db')

# Lego_Set = namedtuple('Lego_Set', ['times_sold', 'total_qty', 'min_price', 'avg_price', 'qty_avg_price', 'max_price'])

# lego_id = str(input("Enter Product ID: "))
# url = 'http://www.bricklink.com/v2/catalog/catalogitem.page?S='+lego_id+'#T=P'
# browser = webdriver.Chrome()
# browser.get(url)
# source = browser.page_source

# soup = BeautifulSoup(source, 'lxml')

# table = soup.find('table', class_='pcipgSummaryTable')



# browser.quit()
# conn.close()






