import time

from selenium import webdriver
import os

import shutil
shutil.rmtree("./listings")
os.mkdir(os.curdir + "/listings")

Search_Item = input("Type a search term: ")

Browser = webdriver.Firefox()

Browser.get("https://www.ebay.com/")

SearchBar = Browser.find_element_by_id("gh-ac")

SearchBar.send_keys(Search_Item)
SearchBar.submit()

time.sleep(4)

for I in range(10):

    time.sleep(1)

    try:

        RightArrow = Browser.find_element_by_xpath("//a[@class='pagination__next icon-link']")
        break

    except:

        if I == 9 :

            print("No right arrow, must be one page or bugged!")

            Browser.quit()
            quit(1)

HighOrLow = input("High or low, type h or l: ") == "h"

LowestPrice = 0 if (HighOrLow) else 999999999
LowestListingPrice = None

while True:

    Listings = Browser.find_elements_by_xpath("//li[@class='s-item s-item--watch-at-corner']")

    for Listing in Listings:

        try:

            Price = float(Listing.find_element_by_class_name("s-item__price").text.replace("$", "").replace(",", ""))

        except:

            print("No PRICE!")

        if (HighOrLow and Price > LowestPrice) or (not HighOrLow and Price < LowestPrice):

            print("New High Price Found! " + str(Price))
            LowestPrice = Price
            LowestListingPrice = Listing

            try:

                LowestListingPrice.screenshot("listings/" + str(Price) + " Lowest " + LowestListingPrice.find_element_by_xpath(".//h3[@class='s-item__title']").text + ".png")

            except:

                print("No title?")

    RightArrow.click()

    for I in range(10):


        try:

            RightArrow = Browser.find_element_by_xpath("//a[@class='pagination__next icon-link']")
            break

        except:

            if I == 9:
                print("No right arrow, must be one page or bugged!")

                Browser.quit()
                quit(1)

        time.sleep(1)

    if RightArrow.get_property("href") == Browser.current_url :

        break



Browser.close()
