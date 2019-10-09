from bs4 import BeautifulSoup
from selenium import webdriver


lego_id = str(input("Enter Product ID: "))
url = 'http://www.bricklink.com/v2/catalog/catalogitem.page?S='+lego_id+'#T=P'
browser = webdriver.Chrome()
browser.get(url)
source = browser.page_source

# f = open("results_"+lego_id+".txt", "w")

# f.write(source)
# f.close()

soup = BeautifulSoup(source, 'lxml')

result = soup.find('table', class_='pcipgSummaryTable')

rows = result.find_all('td')

clean_rows = [];
for row in rows:
	clean_rows.append(row.get_text())

# rows = result.find_all('tr')

# for row in rows:
# 	row.find_all('td')

print result
print "\r\n"
print clean_rows
browser.quit()





