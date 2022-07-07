#!/usr/bin/env python

import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
#from bs4 import BeautifulSoup as soup
#from urllib.request import urlopen


class GolfBot():
    """describes the framework of the automated system"""

    def __init__(self, hr, min, sec, opentime):
        self.hr = hr
        self.min = min
        self.sec = sec
        self.opentime = opentime
        
    def countdown(self, now):
        # TODO -!--> refactor to reduce redundancy
        if int(now[:2]) == self.hr:
            if int(now[3:5]) == min:
                print("T- " +
                    str(self.sec - int(now[6:8])) + " sec")
            else:
                print("T- " +
                    str(self.min - int(now[3:5])) + " min " +
                    str(self.sec - int(now[6:8])) + " sec"  )
        else:
            print("T- " +
                str(self.hr  - int(now[ :2])) + " hr "  +
                str(self.min - int(now[3:5])) + " min " +
                str(self.sec - int(now[6:8])) + " sec"  )
    
    def findTimes(self, webPage, h, m):
        # loop through all possible timeslots, and determine if it can be clicked
        meridian = "A"
        while m < 51:
            if meridian == "P":
                if h > 5:
                    break
            if h > 12:
                h = 1
                meridian = "P"
            
            if not m:
                m = "00"
            if webPage.findLink(f"{h}:{m} {meridian}M"):
                webPage.clickLink(f"{h}:{m} {meridian}M")
                print(f"selected {h}:{m} {meridian}M")
                break
            if not isinstance(m, int):
                m = 0
            m += 10
            if m == 60: m = 0; h += 1


class WebPage():
    """describes a web page for use with selenium"""

    def __init__(self, url, browser="safari"):
        self.url = url
        if browser == "safari":
            self.driver = webdriver.Safari("/usr/bin/safaridriver") # safari executable is found in usr/bin
        else:
            self.driver = webdriver.Chrome("./chromedriver") # chromedriver executable needs to be in the parent directory

    def openPage(self):
        self.driver.get(self.url)

    def closePage(self):
        self.driver.quit()

    # TODO -!--> remove this function, its redundant; no need for it when checking for NoSuchElementException in clickLink()
    def findLink(self, name):
        # locate button by the link text
        if not (self.driver.find_elements(webdriver.common.by.By.LINK_TEXT, name)):
            print(f"{name} not found")
            return False
        # TODO -!--> return false if it doesnt exist
        # might have to use beautiful soup for this
        return self.driver.find_element(webdriver.common.by.By.LINK_TEXT, name)

    def clickLink(self, name=""):
        # locate button by the link text and click it if it exists
        try:
            self.driver.find_element(webdriver.common.by.By.LINK_TEXT, name).click()
        except NoSuchElementException:
            print("Link does not exist")

    def setURL(self, url):
        self.url = url


def main():

    # initialize golfbot instance
    golf = GolfBot(7, 29, 60, "07:30:00")

    teetime = input("Please enter the earliest time you want to play in multiples of 10min (e.g. 7:50): ")

    cwd = os.path.abspath(os.getcwd())
    url = f"file://{cwd}/MemberIdentification.html"
    pageA = WebPage(url, "chrome")
    pageA.openPage()
    pageB = WebPage(url, "chrome")
    pageB.openPage()

    # TODO -!--> move the countdown here once testing is done

    # click austin
    # buttons are <a> tags

    pageA.clickLink("Austin Copley")
    pageB.clickLink("Member 1")
    pageA.clickLink("Sat:")
    pageB.clickLink("Sat:")

    # pass the webpage to the golfbot to locate tee times
    h, m = int(teetime.split(":")[0]), int(teetime.split(":")[1])
    golf.findTimes(pageA, h, m)
    golf.findTimes(pageB, h, m)

    # TODO -!--> either give user opportunity to select their own players and methods of transport, or autofill fields

    # TODO -!--> web scrape with beautifulsoup?
    """client = urlopen(url)
    html = client.read()
    client.close()
    # parse html
    page = soup(html, "html.parser")
    print(page.title) # test that the page title prints correctly"""

    now = time.ctime()[11:19]

    # ---> give user time reference
    while now != golf.opentime:

        golf.countdown(now)

        # ---> stop counting a couple seconds before opentime
        now = time.ctime()[11:19]
        if ( int(now[:2]) == golf.hr ) and ( int(now[3:5]) == golf.min) and ( int(now[6:]) >= golf.sec - 3):
            break
                
        # otherwise, sleep 1 sec
        time.sleep(1)


    # ---> loop until it is exactly 7:30 am
    while time.ctime()[11:19] != golf.opentime:
        continue

    print("golf")
    print(time.ctime()[11:19])


if __name__ == "__main__":
    main()
