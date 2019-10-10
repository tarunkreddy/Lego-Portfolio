from bs4 import BeautifulSoup
from selenium import webdriver
from collections import namedtuple

#creates the Lego_Set named tuple from row data
def createTuples(table):
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




Lego_Set = namedtuple('Lego_Set', ['times_sold', 'total_qty', 'min_price', 'avg_price', 'qty_avg_price', 'max_price'])

lego_id = str(input("Enter Product ID: "))
url = 'http://www.bricklink.com/v2/catalog/catalogitem.page?S='+lego_id+'#T=P'
browser = webdriver.Chrome()
browser.get(url)
source = browser.page_source

# f = open("results_"+lego_id+".txt", "w")

# f.write(source)
# f.close()

soup = BeautifulSoup(source, 'lxml')

table = soup.find('table', class_='pcipgSummaryTable')


print createTuples(table)
browser.quit()






