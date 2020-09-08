from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os.path
import re
import sys
import glob
import time
import datetime

options = webdriver.ChromeOptions()
browser = webdriver.Chrome(r"C:\Users\user\Desktop\chromedriver.exe",chrome_options=options)



return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
one_way_ticket = "//label[@id='flight-type-one-way-label-hp-flight']"
multi_ticket = "//label[@id='flight-type-multi-dest-label-hp-flight']"

def ticket_chooser(ticket):
    try:
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as e:
        pass

def dep_country_chooser(dep_country):
    fly_from = browser.find_element_by_xpath("//*[@id='sb_ifc50']/input") 
    time.sleep(1)
    fly_from.clear()
    time.sleep(1.5)
    fly_from.send_keys('  ' + dep_country)
    time.sleep(1.5)
    first_item = browser.find_element_by_xpath("//*[@id='sbse0']")
    time.sleep(1.5)
    first_item.click()

def arrival_country_chooser(arrival_country):
    fly_to = browser.find_element_by_xpath("//*[@id='sb_ifc50']/input") 
    time.sleep(1)
    fly_to.clear()
    time.sleep(1.5)
    fly_to.send_keys('  ' + arrival_country)
    time.sleep(1.5)
    first_item = browser.find_element_by_xpath("//*[@id='sbse0']") 
    time.sleep(1.5)
    first_item.click()

def dep_date_chooser(date1):
    dep_date_button = browser.find_element_by_xpath("//input[@value]") 
    dep_date_button.clear()
    time.sleep(0.5)
    dep_date_button.send_keys(date1)
    dep_date_button.send_keys(Keys.ENTER)

def return_date_chooser(date2):#//*[@id='flt-modaldialog']/div/div[4]/div[2]/div[3]
    return_date_button = browser.find_element_by_xpath("//input[@value='Wed, 16 Sep']") 
    return_date_button.click()
    return_date_button.clear() 
    for i in range(11):
        return_date_button.send_keys(Keys.BACKSPACE)
    time.sleep(1)
    return_date_button.send_keys(date2)
    #return_date_button.send_keys(Keys.ENTER)

def search():
    search = browser.find_element_by_xpath("//*[@id='flt-modaldialog']/div/div[5]/g-raised-button")
    search.click()
    time.sleep(5)
    print('Results ready!')

def compile_data(df, origin, destination, date1, date2):
    
    button_expand = browser.find_elements(By.XPATH, "//span[contains(@class, 'gws-flights-results')]")

    dep_times = browser.find_elements_by_xpath("//span[@jscontroller and @jsdata and @jsaction]")
    times_list = list(filter(lambda x: (x != ''), [value.text for value in dep_times]))
    dep_times_list = [times_list[2*i] for i in range(int(len(times_list)/2))] 
    print(dep_times_list)
    
    arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]
    arr_times_list = [times_list[2*i+1] for i in range(int(len(times_list)/2))]
    print(arr_times_list)
    
    airlines = browser.find_elements_by_xpath("//span[contains(@class, 'gws-flights__ellipsize')]")
    airlines_list_prev = [value.text for value in airlines]
    airlines_list = [airlines_list_prev[2*i] for i in range(int(len(airlines_list_prev)/2))]
    airlines_op_list = [airlines_list_prev[2 * i+1] for i in range(int(len(airlines_list_prev) / 2))]
    print(airlines_list)
    
    prices = browser.find_elements_by_xpath("//div[contains(@class, 'flt-subhead1 gws-flights-results__price')]")
    price_list_prev = [value.text for value in prices]     
    price_list = [price_list_prev[2*i] for i in range(int(len(price_list_prev)/2))]
    print(price_list)
    
    durations = browser.find_elements_by_xpath("//div[contains(@class, 'gws-flights-results__duration')]")
    durations_list = [value.text for value in durations]
    print(durations_list)
    
    stops = browser.find_elements_by_xpath("//div[contains(@class, 'gws-flights-results__stops')]")
    stops_list = [value.text for value in stops]
    print(stops_list)
    
    layovers = browser.find_elements_by_xpath("//div[contains(@class, 'gws-flights-results__layover-time')]")
    layovers_list = [value.text for value in layovers]
    print(layovers_list)

    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'price' 
    ind = len(df)
    for i in range(len(dep_times_list)):
        try:
            df.loc[ind, 'origin'] = origin
        except Exception as e:
            pass
        try:
            df.loc[ind, 'destination'] = destination
        except Exception as e:
            pass
        try:
           df.loc[ind, 'departure_day'] = date1
        except Exception as e:
            pass
        try:
            df.loc[ind, 'arrival_day'] = date2
        except Exception as e:
            pass
        try:
            df.loc[ind, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[ind, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[ind, 'airline'] = airlines_list[i]
        except Exception as e:
            pass
        try:
            df.loc[ind, 'duration'] = durations_list[i]
        except Exception as e:
            pass
        try:
            df.loc[ind, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[ind, 'layovers'] = layovers_list[i]
        except Exception as e:
            pass
        try:
            df.loc[ind, str(current_price)] = price_list[i]
        except Exception as e:
            pass
        ind = ind + 1
    print('Excel Sheet Created!')

def bulk(origin, destination, d1, d2,destination_time_interval, df):
    date1, date2 = getdates()
    df = pd.DataFrame()
    
    link = 'https://www.google.com/flights'
    browser.execute_script('window.open()')
    browser.switch_to.window(browser.window_handles[0])
    browser.get(link)
    time.sleep(2)
    
    flights_only = browser.find_element_by_xpath("//*[@id='flt-app']/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[1]") 
    flights_only.click()
    ticket_chooser(return_ticket)
    dep_country_chooser(origin)
    time.sleep(1)
    flights_only = browser.find_element_by_xpath("//*[@id='flt-app']/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[2]")
    flights_only.click()
    arrival_country_chooser(destination)
    time.sleep(1)
    flights_only = browser.find_element_by_xpath("//*[@id='flt-app']/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[4]/div[1]")
    flights_only.click()
    dep_date_chooser(date1)     
    time.sleep(2)
    return_date_chooser(date2) 
    time.sleep(2)
    
    search()
    compile_data(df, origin, destination, date1, date2)
    
    
    writer = pd.ExcelWriter('flightexcel.xlsx', engine='openpyxl')
    df.to_excel(writer, index=False)
    #df.to_excel(writer, startrow=len(df)+2, index=False)
    writer.save()
    df.to_csv("myfile.csv")
    time.sleep(10)
    #browser.close()

def getdates():
    date1 = '30 AUG'
    date2 = '21 SEP'
    return date1,date2


def mainFunction(origin, d1, d2, flexibility):
    df = pd.DataFrame()
    cities = ['barcelona','berlin','moscow']
    for city in cities:
        bulk(origin, city, d1, d2, 0, df)
        cities.remove(city)
    #df.to_excel('flightexcel.xlsx')
    browser.close()


mainFunction('istanbul', '30 AUG', '21 SEP', 4)




