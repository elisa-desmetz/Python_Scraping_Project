from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By

from pyvirtualdisplay import Display

from static.models.Ladder import Ladder

import pandas as pd

import time

s=Service('./applications/chromedriver')

# Images won't load in the webdriver to prevent wasting resources
option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs['profile.default_content_settings'] = {'images': 2}
chrome_prefs['profile.managed_default_content_settings'] = {'images': 2}
option.binary_location = "/usr/bin/google-chrome"    #chrome binary location specified here
option.add_argument("--start-maximized") #open Browser in maximized mode
option.add_argument("--no-sandbox") #bypass OS security model
option.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)

# Variables
main_url = 'https://www.dofus.com/fr/mmorpg/communaute/ladder'

ladder_xp = {'df_name':'df_ladder_xp',
             'class_name' : 'general',
            'filter_id':'servers_222',
            'caption':'XP ladder for Ilyzaelle mono server'}
ladder_success = {'df_name':'df_ladder_success',
                  'class_name' : 'success',
            'filter_id':'servers_222',
            'caption':'Success ladder for Ilyzaelle mono server'}
ladder_pvp_solo = {'df_name':'df_ladder_pvp_solo',
                   'class_name' : 'kolizeum',
            'filter_id':'type_solo',
            'caption':'Ladder for 3v3 solo-queue PvP'}
ladder_pvp_duel = {'df_name':'df_ladder_pvp_duel',
                   'class_name' : 'kolizeum',
            'filter_id':'type_duel',
            'caption':'Ladder for 1v1 PvP'}

categories=[ladder_xp,ladder_success,ladder_pvp_solo,ladder_pvp_duel]

# -- Access to the requested ladder page
def open_ladder(browser, category):
    time.sleep(5)
    if browser.find_element(By.CLASS_NAME, "ak-refuse").is_displayed():
        close_cookie = browser.find_element(By.CLASS_NAME, "ak-refuse").click()
        time.sleep(1.5)
    access_ladder = browser.find_element(By.CLASS_NAME, 'ak-section-'+category['class_name']).click()

# -- Access to the requested filtered ladder
def filter_ladder(browser, category):
    time.sleep(0.5)
    filter_server = browser.find_element(By.ID,category['filter_id']).click()
    time.sleep(1.5)

# -- Extract ladder table to Pandas dataframe
def extract_data(browser):
    cols = []
    for col in browser.find_elements(By.XPATH,"//table[contains(@class, 'ak-ladder')]/thead/tr/th"):
        cols.append(col.text)
    data = []
    num_rows = len (browser.find_elements(By.XPATH,"//table[contains(@class, 'ak-ladder')]/tbody/tr"))
    for row in range(num_rows):
        row_data=[]
        for col in browser.find_elements(By.XPATH,"//table[contains(@class, 'ak-ladder')]/tbody/tr["+str(row)+"]/td"):
            row_data.append(col.text)
        if row_data!=[]:
            data.append(row_data)
    return pd.DataFrame(data, columns=cols)

# -- Return the list of dataframes created
def export_dataframes():
    dfs=[]
    # Open browser in fullscreen
    browser = webdriver.Chrome(service=s, options=option)
    browser.maximize_window()
    
    # For every ladder listed in "categories"
    for category in categories :
        # Access main menu URL
        browser.get(main_url)
        # Acces ladder page
        open_ladder(browser, category)
        # Filter ladder table
        filter_ladder(browser, category)
        # Create and stock dataframes
        dfs.append(extract_data(browser))
    
    # Close browser
    browser.quit()
    return dfs

def export_dataframe(category):
    display = Display(visible=0, size=(1027,768))
    
    display.start()
    # Open browser in fullscreen
    browser = webdriver.Chrome(service=s, options=option)
    browser.maximize_window()
    
    # Access main menu URL
    browser.get(main_url)
    # Acces ladder page
    open_ladder(browser, category)
    # Filter ladder table
    filter_ladder(browser, category)
    # Create and stock dataframes
    df = extract_data(browser)
    data = Ladder.to_dict(category['caption'],df)
    # Close browser
    browser.quit()
    display.stop()
    return data
