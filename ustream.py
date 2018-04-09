from selenium import webdriver
import bs4 as BeautifulSoup

browse_url = "http://www.ustream.tv/explore/all"
browser = webdriver.Chrome()
browser.get(browse_url)
html_source = browser.page_source
browser.quit()

soup = BeautifulSoup.BeautifulSoup(html_source, 'html.parser')
viewers = soup.find("div", class_="media-data")

for xd in viewers:
    print(xd.get_text())
