#!/usr/bin/env python

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


class WebPage():
    """describes a web page for use with selenium"""

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome("./chromedriver") # chromedriver executable needs to be in the parent directory
    

    def openPage(self):
        self.driver.get(self.url)

    def closePage(self):
        self.driver.quit()

    def clickMember(self, name="Austin Copley"):
        # locate button
        link = self.driver.find_element(webdriver.common.by.By.LINK_TEXT, name)
        link.click()


def main():
    ##  <<== SELENIUM ==>>
    # TODO -!--> move to after the countdown once testing is done

    url = "file:///Users/austincopley/Downloads/MemberIdentification.html"
    rocc = WebPage(url)
    rocc.openPage()

    # click austin
    # standard_button class <a> tags
    # loop through them and click matching name

    rocc.clickMember("Ellis Copley")

    # TODO -!--> maybe login?
    #           \--> input fields?
    #            print("User logged in")


    # TODO -!--> web scraper with beautifulsoup?
    """client = urlopen(url)
    html = client.read()
    client.close()
    # parse html
    page = soup(html, "html.parser")
    print(page.title) # test that the page title prints correctly"""


    hr = 7
    min = 29
    sec = 60
    opentime = "07:30:00"
    now = time.ctime()[11:19]
    print(time.ctime())

    golf = GolfBot(hr, min, sec, opentime)

    # ---> give user time reference
    while now != opentime:

        golf.countdown(now)

        # ---> stop counting a couple seconds before opentime
        now = time.ctime()[11:19]
        if ( int(now[:2]) == golf.hr ) and ( int(now[3:5]) == golf.min) and ( int(now[6:]) >= golf.sec - 3):
            break
                
        # otherwise, sleep 1 sec
        time.sleep(1)


    # ---> loop until it is exactly 7:30 am
    while time.ctime()[11:19] != opentime:
        continue

    # TODO -!--> register tee time
    print("golf")
    print(time.ctime()[11:19])


if __name__ == "__main__":
    main()
    