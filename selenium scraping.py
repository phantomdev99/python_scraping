from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import csv
import chromedriver_autoinstaller

chromedriver_autoinstaller.install() 

driver = webdriver.Chrome()

def run():
      
    driver.get('https://checkout.xola.com/index.html?xwm=eyJvcmlnaW4iOiJodHRwczovL2JvaXNlLnB1enpsZWVmZmVjdC5jb20iLCJjaGFubmVsIjoiRmJyd2syd2ZxVnFIRHNhTSJ9&canSendPII=false&popup=false&embeddedCheckout=true&xdm=true&gaPage=%2Fbook-now%2F&gaCode=UA-115829360-2&gaClient=482825549.1675815012&xb_session_seller_website=boise.puzzleeffect.com&xb_session_user_id=63e423d2729469a8daacccbb&xb_session_session_id=63e423d2729469a8daacccbc&xdm_e=https%3A%2F%2Fboise.puzzleeffect.com&xdm_c=default8725&xdm_p=1#buttons/5cba1a789806c5082936aca8')

    driver.implicitly_wait(10)

    driver.maximize_window()

    global df

    r=1

    datalist = []
      
    while(1): 
        try:        
            time = driver.find_element("xpath",'//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[1]').text
          
            title = driver.find_element("xpath",'//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[2]/div[2]/div/div[2]/h3').text       
            
            status = driver.find_element("xpath",'//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[2]/div[2]/div/div[3]/div').text

            print(status)

            Data={ 'Time': time,
                   'Title': title,
                   # 'Count': count,
                   'Available': status}
              
            datalist.append(Data)

            df = pd.DataFrame(datalist)   

            r += 1
              
        # if there are no more table data to scrape
        except NoSuchElementException: 
            break
              
    # saving the dataframe to a csv
    df.to_csv('table.csv', index=False) 

driver.find_element("xpath", '//*[@id="header"]/div/div[3]/div/button[2]/i').click()


driver.get('https://checkout.xola.com/index.html?xwm=eyJvcmlnaW4iOiJodHRwczovL2JvaXNlLnB1enpsZWVmZmVjdC5jb20iLCJjaGFubmVsIjoiRmJyd2syd2ZxVnFIRHNhTSJ9&canSendPII=false&popup=false&embeddedCheckout=true&xdm=true&gaPage=%2Fbook-now%2F&gaCode=UA-115829360-2&gaClient=482825549.1675815012&xb_session_seller_website=boise.puzzleeffect.com&xb_session_user_id=63e423d2729469a8daacccbb&xb_session_session_id=63e423d2729469a8daacccbc&xdm_e=https%3A%2F%2Fboise.puzzleeffect.com&xdm_c=default8725&xdm_p=1#buttons/5cba1a789806c5082936aca8')

driver.implicitly_wait(10)

driver.maximize_window()

global df

r=1

datalist = []
  
while(1): 
    try:        
        time1 = driver.find_element("xpath",'//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[1]').text
      
        title = driver.find_element("xpath",'//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[2]/div[2]/div/div[2]/h3').text       
        
        available = driver.find_element("xpath",'//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[2]/div[2]/div/div[3]/div').text

        print(status)

        Data={ 'Time': time1,
               'Title': title,             
               'Available': available}
          
        datalist.append(Data)

        df = pd.DataFrame(datalist)   

        r += 1
          
    # if there are no more table data to scrape
    except NoSuchElementException: 
        break
          
# saving the dataframe to a csv
df.to_csv('table.csv', index=False) 



driver.close()






if __name__=="__main__":
    run()























    --------------------------------------------------




from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import csv
import chromedriver_autoinstaller

chromedriver_autoinstaller.install() 

driver = webdriver.Chrome()

datalist = []

def run():          
        driver.get('https://escapethisboise.com/book-now')

        driver.implicitly_wait(10)

        driver.maximize_window()

        global df

           

          
        week_scrap()

        print("first scraping")

        next_scrap()


def week_scrap():
        time.sleep(3)
        r=1
        while(1): 
            try:
                    
                time1 = driver.find_element('xpath','//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[1]').text
                # time = driver.find_element('xpath','/html/body/div[1]/div/section[3]/section[1]/div[1]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[1]').text
              
                title = driver.find_element('xpath','//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[2]/div[2]/div/div[2]/h3').text       
                # title = driver.find_element("xpath",'/html/body/div[1]/div/section[3]/section[1]/div[1]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[2]/div[2]/div/div[2]/h3').text       
                
                available = driver.find_element('xpath','//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[2]/div[2]/div/div[3]/div').text
                # status = driver.find_element("xpath",'/html/body/div[1]/div/section[3]/section[1]/div[1]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[2]/div[2]/div/div[3]/div').text

                print(time1)

                Data={ 'Time': time1,
                       'Title': title,
                       'Available': available}
                  
                datalist.append(Data)

                df = pd.DataFrame(datalist)   

                r += 1

                print("scraping success!!!")
                  
            # if there are no more table data to scrape
            except NoSuchElementException:
                print("I have some problems -------------------------------")
                break
                  
        # saving the dataframe to a csv
        df.to_csv('table.csv', index=False)

        
          


def next_scrap():
        
        counts = 2

        while(counts<14):
                # driver.get('https://checkout.xola.com/index.html?xwm=eyJvcmlnaW4iOiJodHRwczovL2JvaXNlLnB1enpsZWVmZmVjdC5jb20iLCJjaGFubmVsIjoiRmJyd2syd2ZxVnFIRHNhTSJ9&canSendPII=false&popup=false&embeddedCheckout=true&xdm=true&gaPage=%2Fbook-now%2F&gaCode=UA-115829360-2&gaClient=482825549.1675815012&xb_session_seller_website=boise.puzzleeffect.com&xb_session_user_id=63e423d2729469a8daacccbb&xb_session_session_id=63e423d2729469a8daacccbc&xdm_e=https%3A%2F%2Fboise.puzzleeffect.com&xdm_c=default8725&xdm_p=1#buttons/5cba1a789806c5082936aca8')

                driver.find_element("xpath", '//*[@id="header"]/div/div[3]/div/button[2]').click()

                print("new scraping", counts)

                driver.implicitly_wait(10)

                week_scrap()

                counts += 1

      
 
 
# driver.close()

if __name__=="__main__":
    run()







    






