from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import csv
import chromedriver_autoinstaller
import os
from pathlib import Path
import glob
# from ftplib import FTP

import ftplib
# ftp = ftplib.FTP()

chromedriver_autoinstaller.install() 

options = Options()
options.add_argument("--start-maximized")
# options.headless = True

driver = webdriver.Chrome(options=options)

driver.get('https://www.powerbody.eu/customer/account/login/')

# print(driver.get_cookies())
driver.implicitly_wait(10)

print("login!!!")
email =  driver.find_element("xpath", '//input[@id="login"]').send_keys("info@nutri.se")
driver.implicitly_wait(10)


print("first")
driver.find_element("xpath", '//input[@id="password"]').send_keys("Sonysony2022!")
driver.implicitly_wait(10)

driver.find_element("xpath", '//*[@id="cookie-information"]/p[1]/a').click()

driver.implicitly_wait(10)

driver.find_element("xpath", '/html/body/div[3]/section[1]/div/div/form/div[2]/button').click()

print("button")

print("succeesful")

driver.implicitly_wait(10)

driver.find_element("xpath", '//*[@id="top"]/nav[1]/div/ul[2]/li/a').click()

time.sleep(15)

print("download successful")

currentUser = os.getlogin()

files = glob.glob('C:\\Users\\'+currentUser+'\\Downloads\\*.xls')
path = "C:/Users/"+currentUser+"/Downloads/"
newfilename = path + 'powerbody.xls'
print("recently modified docs", max(files, key=os.path.getctime))

oldfilename = max(files, key=os.path.getctime)
print("Old",os.path.splitext(oldfilename)[0])


os.rename(oldfilename, newfilename)

HOSTNAME = "65.21.141.212"
USERNAME = "developer@amazly.co"
PASSWORD = "xinix123$xinix"

ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

ftp_server.encoding = "utf-8"

dirFTP = "C:/Users/"+currentUser+"/Downloads/"
# toFTP = os.listdir(dirFTP)[0]
toFTP = "powerbody.xls"

print("1",toFTP)
ftp_server.cwd("/public_html/nutri-stock")

# Read file in binary mode
with open(os.path.join(dirFTP,toFTP), "rb") as file:
    # Command for Uploading the file "STOR filename"
    ftp_server.storbinary(f"STOR {toFTP}", file)
print("complete",file)
# Get list of files
ftp_server.dir()
 
# Close the Connection
ftp_server.quit()

os.remove(newfilename)




