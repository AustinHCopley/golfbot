#!/usr/bin/env python

from ctypes.wintypes import HRSRC
import time
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

from selenium import webdriver

class GolfBot():
    """describes the framework of the automated system"""

    def __init__(self, hr, min, sec, opentime):
        self.hr = hr
        self.min = min
        self.sec = sec
        self.opentime = opentime
        

    @classmethod
    def countdown(cls):

        now = time.ctime()[11:19]
        if int(now[:2]) == hr:
            if int(now[3:5]) == min:
                print("T- " +
                    str(sec - int(now[6:8])) + " sec")
            else:
                print("T- " +
                    str(min - int(now[3:5])) + " min " +
                    str(sec - int(now[6:8])) + " sec"  )
        else:
            print("T- " +
                str( hr - int(now[ :2])) + " hr "  +
                str(min - int(now[3:5])) + " min " +
                str(sec - int(now[6:8])) + " sec"  )

        # ---> stop counting a couple seconds before
        

    # otherwise, sleep 1 sec
    time.sleep(1)



class WebPage():
    """describes a web page for use with selenium"""

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome("./chromedriver") # chromedriver executable needs to be in the parent directory
    
    def openPage(self):
        self.drive.get(self.url)


# TODO -!--> move to after the countdown
url = "https://www.roccdallas.com/"
rocc = WebPage(url)
rocc.openPage()


# testing with beautifulsoup
client = urlopen(url)
html = client.read()
client.close()
# parse html
page = soup(html, "html.parser")
print(page.title) # test that the page title prints correctly


hr = 7
min = 29
sec = 60
opentime = "07:30:00"
now = time.ctime()[11:19]
print(time.ctime())

golf = GolfBot(hr, min, sec, opentime)

# ---> give user time reference
while now != opentime:
    golf.countdown()
    now = time.ctime()[11:19]
    if ( int(now[:2]) == golf.hr ) and ( int(now[3:5]) == golf.min) and ( int(now[6:]) >= golf.sec - 3):
            break


# ---> wait until it is 8:00 am
while time.ctime()[11:19] != opentime:
    continue

print("golf")
print(time.ctime()[11:19])

# TODO -!--> connect to website
# TODO -!--> maybe login?
#           \--> input fields?
#            print("User logged in")
# TODO -!--> web scraper?
# TODO -!--> click position/button?

if __name__ == "__main__":
    pass