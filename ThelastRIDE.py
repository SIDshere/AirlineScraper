#all the important libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import re
from random import randint
import pandas as pd
import numpy as np
from time import sleep, strftime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, timedelta, datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options = Options()

def my_destinations(origin,destination, startdate, enddate):
    global results
    #here we created our URL based on inputs
    enddate = datetime.strptime(startdate, '%Y-%m-%d').date() + timedelta(days=0)
    enddate = enddate.strftime('%Y-%m-%d')
    #URL is created here in URL1
    url1 = "https://www.kayak.co.in/flights/" + origin + "-" + destination + "/" + startdate + "/" + enddate + "?sort=price_a"
    print("\n" + url1)

    #here we used chromedriver to access the URL
    options = Options()
    options.binary_location = "E:\\programs\\Google\\Chrome\\Application\\chrome.exe" #original chrome destination
    driver = webdriver.Chrome(chrome_options = options, executable_path=r'E:\DATASCIENCEE\HBSU\SEM II\Chromedriver\chromedriver.exe')
    driver.get(url1)  #link surf website
     
    #this will click on that load more buttin
    driver.implicitly_wait(1) 
    #to load more button
    i=1
    while True:
        try:
            time.sleep(10)
            more_results='ULvh' #change this ID constantly        
            #driver.find_element(By.CLASS_NAME, more_results).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, more_results))).click()
        except:
            print("No more LOAD MORE RESULTS button to be clicked")
            break
    #this will return that whole content block in webelement form
    time.sleep(20)

    a=driver.find_elements(By.XPATH, '//div[@class="nrc6-inner"]') #dont forget to check and change this class


    #we created empty list to save all the data 
    lst_prices = []
    lst_company_names=[]
    timing=[]
    stopss=[]
    airportlist=[]
    hours_total=[]

    #to use beautiful soup 
    soup=BeautifulSoup(driver.page_source, 'lxml')

    for webElements in a:
        elementHTML=webElements.get_attribute('outerHTML')
        elementSoup=BeautifulSoup(elementHTML, 'html.parser')

        #price
        temp_price = elementSoup.find("div", {"class": "Oihj"})
        price = temp_price.find("div", {"class": "f8F1-price-text"})
        lst_prices.append(price.text)

        #company name
        company_names = elementSoup.find("div", {"class": "J0g6-operator-text"}).text
        lst_company_names.append(company_names)

        #dept_time
        timinga = elementSoup.find("div",{"class": "vmXl vmXl-mod-variant-large"}).text
        timing.append(timinga)
        
        #stops
        stopsa = elementSoup.find("span", {"class":"JWEO-stops-text"}).text
        stopss.append(stopsa)

        #total journy hours
        hourss = elementSoup.find("div", {"class":"xdW8 xdW8-mod-full-airport"}).text
        hours_total.append(hourss)
        #name of airport
        #for x in driver.find_elements(By.XPATH, '//*[@id="aLoK"]/div/div[1]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[2]/div/div[2]/span'):
        #    print(x.text)

        #names of airports
        air_name = elementSoup.find("div", {"class" : "c_cgF c_cgF-mod-variant-full-airport"})
        for x in air_name.find_all("span", {"class": "EFvI-ap-info"}):
            airportlist.append(x)

    df=pd.DataFrame({"Origin_Dest" : origin,
                 "Destination" : destination,
                "Company_names" : lst_company_names,
                 "Stops" : stopss,
                 "Timings" : timing,    
                 "Duration" : hours_total,
                 "Price" : lst_prices}
                  )
    return df

my_destinations("BOM", "COK","2023-04-20", "2023-05-22")

































































