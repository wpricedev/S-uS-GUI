from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4 as BeautifulSoup

browse_url = "http://www.ustream.tv/explore/all"

options = Options()
options.add_argument('--headless')
options.add_argument('--mute-audio')

driver = webdriver.Chrome(chrome_options=options)

driver.get(browse_url)
html_source = driver.page_source
driver.quit()

soup = BeautifulSoup.BeautifulSoup(html_source, 'html.parser')
#########################################################################################################
# Get all broadcaster titles from the 'all' browse
#########################################################################################################
for h4 in soup.find_all('h4', class_="item-title"):
    print(h4.find("a")['title'])
#########################################################################################################
# Get all broadcaster viewers from the 'all' browse
#########################################################################################################
for viewers in soup.find_all('span', class_="item-viewers"):
    print(viewers.text)
#########################################################################################################
# Get all broadcaster url from the 'all' browse
#########################################################################################################
for url in soup.find_all('h4', class_="item-title"):
    url_string = url.find("a")['href']
    print("www.ustream.tv" + url_string)
#########################################################################################################
# Get all broadcaster thumbnails from the 'all' browse
#########################################################################################################
for thumbnail in soup.find_all('div', class_="item-image"):
    print(thumbnail.find("img")['src'])
