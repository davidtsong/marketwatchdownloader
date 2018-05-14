from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import pandas as pd
import time, glob, os

def downloadStuffs(username, password):
    options = Options()
    options.set_headless(headless=True)


    profile = webdriver.FirefoxProfile()
    profile.set_preference("webdriver.load.strategy", "unstable")
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", '/Users/david/Programming/Python/marketwatchcharts/')
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # profile = webdriver.ChromeOptions()
    # profile.add_argument("browser.download.folderList", 2)
    # profile.add_argument("browser.download.manager.showWhenStarting", False)
    # profile.add_argument("browser.download.dir", '/Users/david/Programming/Python/marketwatchcharts/')
    # profile.add_argument("browser.helperApps.neverAsk.saveToDisk", "text/csv")


    driver = webdriver.Firefox(firefox_options=options, firefox_profile = profile, executable_path='/usr/bin/geckodriver')

    username = username
    password = password

    driver.get("https://accounts.marketwatch.com/login?target=http%3A%2F%2Fwww.marketwatch.com%2F")
    username_field = driver.find_element_by_class_name("username")
    password_field = driver.find_element_by_class_name("password")
    login_button = driver.find_element_by_class_name("basic-login-submit")

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    delay = 15
    try:
        myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile__name')))
    except TimeoutException:
        print('Too much time')

    driver.get("https://www.marketwatch.com/game/gbhs-ap-econ-stock-project/portfolio")

    # delay = 1
    # try:
    #     myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'download__data')))
    # except TimeoutException:
    #     print('Too much time')

    # transactionsTable = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'portfolio-performance')))
    # ActionChains(driver).move_to_element(transactionsTable).perform()
    #transactions = driver.find_elements_by_css_selector(".download__data")
    # transactions = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'download__data')))
    # transactions.click()
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # source_element = driver.find_element_by_xpath("//a[.='Download']")
    # source_element = driver.find_element_by_xpath("//div[@class='download__data align--right']/a")
    # ActionChains(driver).move_to_element(source_element).perform()
    #Download CSV Files
    delay = 15
    try:
        myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'download__data')))
    except TimeoutException:
        print('Too much time')

    transactions = driver.find_elements_by_xpath("//div[@class='download__data align--right']/a")
    y=transactions[0].location_once_scrolled_into_view['y']
    y+=800
    driver.execute_script("window.scrollTo(0,{y})".format(y=y))
    transactions[0].click()

    time.sleep(2)

    x=transactions[1].location_once_scrolled_into_view['y']
    x+=1500
    driver.execute_script("window.scrollTo(0,{x})".format(x=x))
    transactions[1].click()

    time.sleep(2)

    #Get files and make into binary pass and delete when done
    overallPath = glob.glob('Portfolio Performance*.csv')[0]
    transactionsPath = glob.glob('Portfolio Transactions*.csv')[0]

    overall = pd.read_csv(overallPath)
    transactions = pd.read_csv(transactionsPath)

    os.remove(overallPath)
    os.remove(transactionsPath)
    driver.close()

    return [overall,transactions]
