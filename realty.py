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

# global df
df = pd.DataFrame()

def run():          
		driver.get("https://search.rebaterealty.com/idx/results/listings?idxID=d025&pt=1&a_propStatus%5B%5D=Active&start=1")

		driver.implicitly_wait(10)

		driver.maximize_window()


		print("first scraping")
		count = 1
		week_scrap(count)

		# print("first scraping")

		next_scrap()


def week_scrap(count):
		# time.sleep(3)
		counts = count
		r=1
		while(1): 
			try:
				driver.get("https://search.rebaterealty.com/idx/results/listings?idxID=d025&pt=1&a_propStatus%5B%5D=Active&start=" + str(counts))
					
				# listingId = driver.find_element("xpath",'//*[@id="content"]/div/div/div[1]/div/div['+str(r)+']/div/div/div/div[1]').text
				listingId_attr = driver.find_element("xpath",'//*[@id="IDX-resultsActiveListings"]/div/div['+str(r)+']')
				# listingId_attr = driver.find_element("xpath",'//*[@id="IDX-resultsActiveListings"]/div/div[1]')

				
							   
				listingId = listingId_attr.get_attribute('data-listingid')
				
				print("listingID:::::", listingId)

				# finalUrl = driver.find_element("xpath",'//*[@id="IDX-resultsActiveListings"]/div/div['+str(r)+']/div/div[1]/div[2]/div[1]/div/a').get_attribute('href')
				finalUrl = driver.find_element("xpath",'//*[@id="IDX-resultsActiveListings"]/div/div['+str(r)+']/div/div[1]/div[2]/div[1]/div/a').get_attribute('href')
				print("finalUrl", finalUrl)

				driver.find_element("xpath", '//div[@id="IDX-resultsActiveListings"]/div/div['+str(r)+']/div/div[1]/div[2]/div[1]/div/a').click()
				driver.find_element("xpath", '//div[@id="IDX-detailsImage-1"]').click()
				
				imageUrl = driver.find_element("xpath", '//div[@id="IDX-photoGalleryImage-1"]/img').get_attribute('src')
				print("imageUrl::::", imageUrl)

				cityName = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[1]/ul/li[4]/span[1]').text
				
				print("cityName::::", cityName)

				driver.find_element("xpath", '//a[@id="IDX-goToProperty"]').click()

				listingName = driver.find_element("xpath", '//*[@id="IDX-detailsAddress"]').text
				print("listingName:::::::::::", listingName)
				driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[5]/ul/li[2]').click()

				description = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[5]/div/div[1]').text
				print("description:::", description)

				# bedrooms = driver.find_element("xpath", '//*[@id="IDX-bedrooms"]/span[1]').text


				# fullbaths = driver.find_element("xpath", '//*[@id="IDX-fullBaths"]/span[1]').text

				# partialBaths = driver.find_element("xpath", '//*[@id="IDX-partialBaths"]/span[1]').text

				# sqft = driver.find_element("xpath", '//*[@id="IDX-sqFt"]/span[1]').text
				# print("This is description-------")

				
				
				

				price = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[3]/div[6]/span[2]').text
				print("price:::", price)

				driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[5]/ul/li[3]').click()

				propertyType = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[5]/div/div[3]/div[2]/div[2]/span').text
				print("propertyType::::", propertyType)

				driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[5]/ul/li[8]').click()


				listingType = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[5]/div/div[8]/div[2]/div/span').text
				print("listingType", listingType)
				

				context_address_num = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[3]/div[3]/div[1]/span[1]').text
				context_address_name = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[3]/div[3]/div[1]/span[3]').text
				context_address_city = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[3]/div[3]/div[2]/span[1]').text
				context_address_state = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[3]/div[3]/div[2]/span[2]').text
				context_address_stateabrv = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[3]/div[3]/div[2]/span[3]').text
				context_address_zipcode = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[3]/div[3]/div[2]/span[4]').text
				context_address_zip4 = driver.find_element("xpath", '/html/body/div[1]/div/div/article/div/div/div[2]/div[3]/div/div[3]/div[3]/div[2]/span[5]').text

				contextualKeywords = context_address_num + ' ' +context_address_name + ' ' +context_address_city + ' ' +context_address_zipcode
				print("contextKeywords::::::", contextualKeywords)
				# contextualKeywords1 = driver.find_element("xpath", '')
				
				address = context_address_city + ' ' +  context_address_state + context_address_stateabrv + context_address_zipcode + context_address_zip4

				print("address:::::", address)

				# acresElement = driver.find_element("xpath", '//*[@id="IDX-acres"]/span[1]')

				# try :
				# 	acres = driver.find_element("xpath", '//*[@id="IDX-acres"]/span[1]').text
				# 	print("acres::::", acres)
				# except NoSuchElementException:
				# 	acres = '0'
				# 	print("acres::::", acres)
				# 	# break

				# description = bedrooms + " Bedroom and " + fullbaths + " Full Bathroom with " + partialBaths + "Partial bathrooms.The house has " + sqft + " Square feet living square feet located on " + acres + " Acres lot."

				# print("description:::", description)

				Data={ 'Listing ID': listingId,
					'Listing Name': listingName,
					'Final URL': finalUrl,
					'Image URL': imageUrl,
					'City Name': cityName,
					'Description': description,
					'Price': price,
					'Property Type': propertyType,
					'Listing Type': listingType,
					'Contextual Keywords': contextualKeywords,
					'Address': address}
					
				datalist.append(Data)

				df = pd.DataFrame(datalist)   

				r += 1

				print("scraping success!!!")
					
			# if there are no more table data to scrape
			except NoSuchElementException:
				print("There is no element you are goint to find -------------------------------")
				break	
				  
		# saving the dataframe to a csv
		df.to_csv('table.csv', index=False)

		
		  


def next_scrap():
		
        counts = 1

        while(counts<21):
                driver.get("https://search.rebaterealty.com/idx/results/listings?idxID=d025&pt=1&a_propStatus%5B%5D=Active&start=" + str(counts))

                # driver.get('https://checkout.xola.com/index.html?xwm=eyJvcmlnaW4iOiJodHRwczovL2JvaXNlLnB1enpsZWVmZmVjdC5jb20iLCJjaGFubmVsIjoiRmJyd2syd2ZxVnFIRHNhTSJ9&canSendPII=false&popup=false&embeddedCheckout=true&xdm=true&gaPage=%2Fbook-now%2F&gaCode=UA-115829360-2&gaClient=482825549.1675815012&xb_session_seller_website=boise.puzzleeffect.com&xb_session_user_id=63e423d2729469a8daacccbb&xb_session_session_id=63e423d2729469a8daacccbc&xdm_e=https%3A%2F%2Fboise.puzzleeffect.com&xdm_c=default8725&xdm_p=1#buttons/5cba1a789806c5082936aca8')
                print("======================")
                driver.find_element("xpath", '//*[@id="IDX-resultsPager-header"]/div[3]').click()
                counts += 1
                print("new scraping", counts)

                driver.implicitly_wait(10)

                week_scrap(counts)

                

	  
 
 
# driver.close()

if __name__=="__main__":
	run()







	






