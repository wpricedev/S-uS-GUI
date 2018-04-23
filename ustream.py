from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4 as BeautifulSoup
#########################################################################################################
# Set up selenium for virtual browsing, thus enabling us to look at the lists
#########################################################################################################
# ToDo: Figure out a way of scrolling/clicking the 'load more' button

class SetUpPageSearch:
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
    def get_info(message):
        browse_url = message
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
        #########################################################################################################
        # Get all broadcaster viewers from the 'all' browse
        #########################################################################################################
        for viewers in soup.find_all('span', class_="item-viewers"):
            broadcaster_viewers.append(viewers.text)
        #########################################################################################################
        # Get all broadcaster url from the 'all' browse
        #########################################################################################################
        for url in soup.find_all('h4', class_="item-title"):
            url_string = url.find("a")['href']
            broadcaster_url.append("www.ustream.tv" + url_string)
        #########################################################################################################
        # Get all broadcaster thumbnails from the 'all' browse
        #########################################################################################################
        for thumbnail in soup.find_all('div', class_="item-image"):
            broadcaster_thumbnail.append(thumbnail.find("img")['src'])
        #########################################################################################################
        # Manage list elements & return lists
        #########################################################################################################
        broadcaster_viewers = [temp.replace('\n', '') for temp in broadcaster_viewers]
        # ^uStream HTML adds a newline by default, this removes that pesky newline^
        return broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail


class BrowseUpcoming:
    @staticmethod
    def get_info(message):
        browse_url = message
        soup = BeautifulSoup.BeautifulSoup((SetUpPage.get_page(browse_url)), 'html.parser')

        broadcaster_title = []
        broadcaster_date = []
        broadcaster_url = []
        broadcaster_thumbnail = []

        for p in soup.find_all('p', class_="pageitem-title"):
            broadcaster_title.append(p.text)

        for date in soup.find_all('p', class_="page-date"):
            broadcaster_date.append(date.text)

        for p in soup.find_all('p', class_="pageitem-title"):
            url_string = p.find("a")['href']
            broadcaster_url.append("www.ustream.tv" + url_string)

        for thumbnail in soup.find_all('a', class_="iwrp media-swap"):
            broadcaster_thumbnail.append(thumbnail.find("img")['src'])

        broadcaster_title = [temp.replace('\n', '') for temp in broadcaster_title]
        broadcaster_title = [temp.replace('\t', '') for temp in broadcaster_title]
        # The broadcaster title on the site is heavily infested with '\n and \t tags
        broadcaster_date = [temp.replace('\n', '') for temp in broadcaster_date]
        return broadcaster_title, broadcaster_date, broadcaster_url, broadcaster_thumbnail


class ViewProfile:
    @staticmethod
    def get_info(message):
        browse_url = message
        soup = BeautifulSoup.BeautifulSoup((SetUpPage.get_page(browse_url)), 'html.parser')

        broadcaster_title = ""
        broadcaster_description = ""

        for h1 in soup.find_all('h1', class_="title"):
            broadcaster_title = h1.text

        for article in soup.find_all('article', class_="description"):
            broadcaster_description = article.text

        return broadcaster_title, broadcaster_description

# message = "http://www.ustream.tv/nasahdtv"
# ViewProfile.get_info(message)
