from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4 as BeautifulSoup
#########################################################################################################
# Set up selenium for virtual browsing, thus enabling us to look at the lists
#########################################################################################################
# ToDo: Create multiple urls (using /ALL, not the default url) that utilise the below script
# ToDo: Create a new script for the Upcoming page, which is quite different to the others
# ToDo: Create scripts for recently viewed & following
# ToDo: Create script for profile page
# ToDo: Figure out a way of scrolling/clicking the 'load more' button


class SetUpPage:
    @staticmethod
    def get_page(url):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--mute-audio')

        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)

        url = driver.page_source
        driver.quit()
        return url


class BrowseAll:
    @staticmethod
    def get_info():
        browse_url = "http://www.ustream.tv/explore/all"
        #########################################################################################################
        # Set up BeautifulSoup with the page opened by selenium previously
        #########################################################################################################
        soup = BeautifulSoup.BeautifulSoup((SetUpPage.get_page(browse_url)), 'html.parser')
        #########################################################################################################
        # Get all broadcaster titles from the 'all' browse
        #########################################################################################################
        broadcaster_title = []
        broadcaster_viewers = []
        broadcaster_url = []
        broadcaster_thumbnail = []
        #########################################################################################################
        # Get all broadcaster titles from the 'all' browse
        #########################################################################################################
        for h4 in soup.find_all('h4', class_="item-title"):
            broadcaster_title.append(h4.find("a")['title'])
            #print(h4.find("a")['title'])
        #########################################################################################################
        # Get all broadcaster viewers from the 'all' browse
        #########################################################################################################
        for viewers in soup.find_all('span', class_="item-viewers"):
            broadcaster_viewers.append(viewers.text)
            #print(viewers.text)
        #########################################################################################################
        # Get all broadcaster url from the 'all' browse
        #########################################################################################################
        for url in soup.find_all('h4', class_="item-title"):
            url_string = url.find("a")['href']
            broadcaster_url.append("www.ustream.tv" + url_string)
            #print("www.ustream.tv" + url_string)
        #########################################################################################################
        # Get all broadcaster thumbnails from the 'all' browse
        #########################################################################################################
        for thumbnail in soup.find_all('div', class_="item-image"):
            broadcaster_thumbnail.append(thumbnail.find("img")['src'])
            #print(thumbnail.find("img")['src'])
        #########################################################################################################
        # Manage list elements & return lists
        #########################################################################################################
        broadcaster_viewers = [temp.replace('\n', '') for temp in broadcaster_viewers]
        #^uStream HTML adds a newline by default, this removes that pesky newline^
        #print(broadcaster_title[0])
        #print(broadcaster_viewers[0])
        #print(broadcaster_url[0])
        #print(broadcaster_thumbnail[0])
        return broadcaster_title, broadcaster_viewers, browse_url, broadcaster_thumbnail


#BrowseAll.get_info()
