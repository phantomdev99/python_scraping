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
from pandas import ExcelFile
import glob
import xlrd
import math
# from ftplib import FTP

import ftplib
# ftp = ftplib.FTP()

HOSTNAME = "65.21.141.212"
USERNAME = "developer@amazly.co"
PASSWORD = "xinix123$xinix"

ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

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
newfilename = path + 'oldpowerbody.xls'
print("recently modified docs----------------------", max(files, key=os.path.getctime))

oldfilename = max(files, key=os.path.getctime)
print("Old------------------------------",os.path.splitext(oldfilename)[0])

os.rename(oldfilename, newfilename)

workbook = xlrd.open_workbook_xls("C:/Users/" +currentUser+ "/Downloads/oldpowerbody.xls", ignore_workbook_corruption=True)

data = pd.read_excel(workbook)
df = pd.DataFrame(data)


# df = df.drop('', axis = 1, inplace=True)
df = df.iloc[8:9630, 8:13]

df1 = df.iloc[ : , 0:1 ]
df2 = df.iloc[ : , 4:5 ]
# df2 = df2.replace(['+'], '')
# if df2.values == null :
# print(df1)
df1Temp = []
df2Temp = []
for  attr in df1.values:
    if type(attr[0]) is float:
        attr[0] = "none"
    df1Temp.append(attr[0])
del df1Temp[0]
df1 = pd.DataFrame(df1Temp, columns=['SKU'])

for  attr in df2.values:
    if type(attr[0]) is float:
        attr[0] = "0"
    df2Temp.append(attr[0].replace('+',''))
del df2Temp[0]
df2 = pd.DataFrame(df2Temp, columns=['QTY'])

# DF = df1.append()
frame = [df1, df2]
df3 = pd.concat(frame,axis="columns").set_index('SKU')
df3 = df3.iloc[ 1:9619, : ]
print(df3)

df4 = df3.iloc[0:1, :]
df5 = df3.iloc[2:9631, :]
# df3 =df.drop([0,2], axis=1)
# df = df.drop(1, axis=1)
print("+++++++++++++++",df2)
df6 = pd.concat([df4, df5], axis="rows", ignore_index=False)

print(df6)

df6.to_excel('C:/Users/' +currentUser+ '/Downloads/powerbody.xls')
os.remove(newfilename)

# Download csv file to local downloads directory.

filename = "saldo.csv" # get filenames within the directory
print (filename)
ftp_server.cwd("/public_html/nutri-stock")

local_filename = os.path.join('C:/Users/' +currentUser+ '/Downloads/', filename)
file = open(local_filename, 'wb')
ftp_server.retrbinary('RETR '+ filename, file.write)

# data = pd.read_csv('C:/Users/' +currentUser+ '/Downloads/saldo.csv')
file.close()


#### get csv file data to local ####

df_csv = pd.read_csv('C:/Users/' +currentUser+ '/Downloads/saldo.csv', encoding= 'unicode_escape',sep=';',engine='python')


# data = pd.DataFrame(df, columns = ['ArticleNo','ArticleName', 'SellableNumberOfItems'] ).set_index('ArticleNo')
csv_data = pd.DataFrame(df_csv)

csv_first = csv_data.iloc[0:, 0:1]
csv_second = csv_data.iloc[0:, 1:2]
csv_third = csv_data.iloc[0:, 2:3]

csv_first_object = []
csv_second_object = []
csv_third_object = []

csv_first_object = csv_first.values
csv_second_object = csv_second.values
# csv_third_object = csv_third.values

for attr in csv_third.values:
    csv_third_object.append(str(attr[0]).replace(',','').replace('"',''))

#### get excel file data to local ####

workbook = xlrd.open_workbook_xls("C:/Users/" +currentUser+ "/Downloads/powerbody.xls", ignore_workbook_corruption=True)

excel_data = pd.read_excel(workbook)

result_excel = pd.DataFrame(excel_data)

excel_first_obj = []
excel_second_obj = []

excel_first = result_excel.iloc[0:, 0:1]
excel_second = result_excel.iloc[0:, 1:2]

excel_first_obj = excel_first.values
excel_second_obj = excel_second.values

print(excel_first_obj)
print(excel_second_obj)

print("rows-length===================", len(result_excel))
print("rows-length===================", len(csv_data))
# print("excel result ============",result)



#### prepare implement ####

for i in range(len(csv_data)):
    if csv_first_object[i][0][0] == "P":

        for j in range(len(result_excel)):
            # print("TYPE:TYPE:TYPE:TYPE:TYPE:TYPE:TYPE:::",type(int(csv_third_object[i])),type(excel_second_obj[j][0]))
            if csv_first_object[i] == excel_first_obj[j]:
                print(i,j)
                if int(csv_third_object[i]) < excel_second_obj[j][0]:

                    
                    csv_third_object[i] = excel_second_obj[j][0]

                    print("successful--------------- prepare implement",csv_third_object[i], excel_second_obj[j][0])
                else:
                    print("failed-----------------:::", csv_first_object[i][0], excel_first_obj[j][0])

            # else:
                # print("preparing...", csv_first_object[i], excel_first_obj[j])
    else:
        # break
        print("I have jump!!!!!!!!!!!!!!!!")

result_csv_1 = pd.DataFrame(csv_first_object, columns=["ArticleNo"])
result_csv_2 = pd.DataFrame(csv_second_object, columns=["ArticleName"])
result_csv_3 = pd.DataFrame(csv_third_object, columns=["SellableNumberOfItems"])

result_csv = pd.concat([result_csv_1, result_csv_2, result_csv_3], axis=1)

result_csv.to_csv('C:/Users/'+currentUser+'/Downloads/nutri-stock.csv')




ftp_server.encoding = "utf-8"

dirFTP = "C:/Users/"+currentUser+"/Downloads/"
# toFTP = os.listdir(dirFTP)[0]
toFTP = "powerbody.xls"

# print("1-----------------------",toFTP)




# Read file in binary mode
with open(os.path.join(dirFTP,toFTP), "rb") as file:
    # Command for Uploading the file "STOR filename"
    ftp_server.storbinary(f"STOR {toFTP}", file)
print("complete",file)


# Upload on ftp server csv file.
dirFTP_csv = "C:/Users/"+currentUser+"/Downloads/"
# toFTP = os.listdir(dirFTP)[0]
toFTP_csv = "nutri-stock.csv"


with open(os.path.join(dirFTP_csv,toFTP_csv), "rb") as file:
    # Command for Uploading the file "STOR filename"
    ftp_server.storbinary(f"STOR {toFTP_csv}", file)
print("complete",file)

# Get list of files
ftp_server.dir()
 
# Close the Connection
ftp_server.quit()

os.remove('C:/Users/' +currentUser+ '/Downloads/saldo.csv')

os.remove("C:/Users/" +currentUser+ "/Downloads/nutri-stock.csv")

os.remove("C:/Users/" +currentUser+ "/Downloads/powerbody.xls")




