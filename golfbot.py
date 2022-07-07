#!/usr/bin/env python

import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


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

    def timedLaunch(self):

        now = time.ctime()[11:19]

        while now != self.opentime:

            self.countdown(now)

            # ---> stop counting a couple seconds before opentime
            now = time.ctime()[11:19]
            if ( int(now[:2]) == self.hr ) and ( int(now[3:5]) == self.min) and ( int(now[6:]) >= self.sec - 3):
                break
                
            # otherwise, sleep 1 sec
            time.sleep(1)

        # ---> loop until it is exactly 7:30 am
        while time.ctime()[11:19] != self.opentime:
            continue

        print("golf")
        print(time.ctime()[11:19])


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

    def findLink(self, name):
        # locate button by the link text
        if not (self.driver.find_elements(webdriver.common.by.By.LINK_TEXT, name)):
            print(f"{name} not found")
            return False
            
        return self.driver.find_element(webdriver.common.by.By.LINK_TEXT, name)

    def clickLink(self, name=""):
        # locate button by the link text and click it if it exists
        try:
            self.driver.find_element(webdriver.common.by.By.LINK_TEXT, name).click()
        except NoSuchElementException:
            # if link can't be found
            print("Link does not exist")
            time.sleep(0.5)
            self.clickLink(name)

    def loginButton(self):
        url = "./MemberIdentification.html"
        #url = "/SiteDesign/ForeTeesScript.aspx"
        self.driver.find_element(webdriver.common.by.By.XPATH,f'//a[contains(@href,"{url}")]').click()

    def setURL(self, url):
        self.url = url


def main():

    # initialize golfbot instance
    golf = GolfBot(7, 29, 60, "07:30:00")

    teetime = input("Please enter the earliest time you want to play in multiples of 10min (e.g. 7:50): ")
    date = input("Please enter the day of the month to schedule (e.g. 16): ")

    cwd = os.path.abspath(os.getcwd())
    url = f"file://{cwd}/MemberIdentification.html"
    pageA = WebPage(url, "chrome")
    pageA.openPage()

    # TODO -!--> move the countdown here once testing is done, or move it after a refresh calendar click
    # TODO -!--> login to renew session

    # click austin
    # all buttons are <a> tags
    time.sleep(1)
    pageA.clickLink("Austin Copley")
    # click on the inputted date
    time.sleep(1)
    pageA.clickLink(date)
    time.sleep(1)

    # pass the webpage to the golfbot instance to locate tee times
    h, m = int(teetime.split(":")[0]), int(teetime.split(":")[1])
    golf.findTimes(pageA, h, m)

    # TODO -!--> either give user opportunity to select their own players and methods of transport
    #            or autofill fields, or leave the page open for the user to do it manually

    # ---> give user time reference while waiting for schedule to open
    golf.timedLaunch()

    input("Press Enter to end program and close browser...")

    pageA.closePage()

if __name__ == "__main__":
    main()
