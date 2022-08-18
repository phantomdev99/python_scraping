import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import random
import time
import hashlib
import hmac
import requests
from datetime import datetime, timezone, timedelta
from dicttoxml import dicttoxml
import traceback
import math
from random import randint
from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from ftplib import FTP

ftp = FTP('racingbang.com', user='techypin@racingbang.com', passwd='P#1998iyush')
last_auth_time = 0
pool = ThreadPoolExecutor(max_workers=8)


def run():
    driver = get_driver()
    driver.get('https://new.dynamicodds.com/')
    delay(2, 3)
    print('[+] log in...')
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys("soonyinyin")
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys("147147qwe")
    driver.find_element(By.XPATH, "//button[text()='Sign In']").click()
    max_retry = 10
    retry = 0
    while retry < max_retry:
        try:
            if int(time.time()) - last_auth_time > 3300:
                token = get_token()
            date = datetime.now(timezone.utc).strftime('%Y-%m-%dT00:00:00.000Z')
            races = get_races(token, date)

            races_data = []
            feed_rows = []
            for race in races:
                feed_rows.append((race, token))
            start2 = time.time()
            futures = [pool.submit(get_bets, args) for args in feed_rows]
            wait(futures, timeout=10, return_when=ALL_COMPLETED)
            print('Fetched {} meetings in {} seconds'.format(
                len(feed_rows), convert_time(time.time()-start2)))
            for res in futures:
                data = res.result()
                races_data.append(data)

            xml = dicttoxml(races_data)
            with open('horse_new.xml', 'wb') as f:
                f.write(xml)
            upload_file()
        except Exception as err:
            print('Error', err)
            retry += 1
            traceback.format_exc()
        finally:
            randSec = randint(5, 15)
            print(f'wait for {randSec} seconds...')
            sleep(randSec)

    driver.quit()


def get_driver():
    print('[+] Opening browser...')
    options = uc.ChromeOptions()
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    options.add_argument("--no-default-browser-check")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.headless=True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    return driver


def get_token():
    global last_auth_time
    try:
        f = open('auth', 'r')
        token, ttime = f.read().strip().split(',')
        f.close()
        if int(time.time()) - int(ttime) < 3000:
            last_auth_time = int(ttime)
            return "Bearer " + token
    except:
        pass

    burp0_url = "https://cognito-idp.ap-southeast-2.amazonaws.com:443/"
    burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"98\"", "X-Amz-User-Agent": "aws-amplify/0.1.x js", "Content-Type": "application/x-amz-json-1.1", "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
                     "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Origin": "https://new.dynamicodds.com", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://new.dynamicodds.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
    burp0_json = {"AuthFlow": "USER_PASSWORD_AUTH", "AuthParameters": {"PASSWORD": "147147qwe",
                                                                       "USERNAME": "soonyinyin"}, "ClientId": "5t4mkoub9779gok9137tlcp7mu", "ClientMetadata": {}}
    r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
    res = r.json()
    f = open('auth', 'w')
    f.write('{},{}'.format(res['AuthenticationResult']
            ['AccessToken'], int(time.time())))
    f.close()
    last_auth_time = int(time.time())
    print('[+] Logged In :', res['AuthenticationResult']['AccessToken'])
    return "Bearer "+res['AuthenticationResult']['AccessToken']



def delay(s, e):
    interval = random.uniform(s, e)
    time.sleep(interval)


def convert_time(cur_time):
    return math.floor(float(cur_time)*100)/100



def generate_hash(my):
    key = "YmV0bWFrZXJzaXN0aGVncmVhdGVzdGNvbXBhbnlpbnRoZXdvcmxk"
    byte_key = bytes(key, 'UTF-8')
    message = my.encode()
    h = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return h


def get_races(token, date):
    ts = str(int(time.time()))
    burp0_headers = {"Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"98\"", "Accept": "*/*",
                     "Content-Type": "application/json", "Authorization": token, "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://new.dynamicodds.com", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://new.dynamicodds.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    burp0_json = {"operationName": None, "query": "{\n  meetingsDated(date: \""+date+"\") {\n    id\n    type\n    date\n    tabIndicator\n    railPosition\n    externalIDs(sources: \"gbs\") {\n      id\n      __typename\n    }\n    track {\n      name\n      country\n      state\n      __typename\n    }\n    races {\n      id\n      class\n      distance\n      name\n      number\n      startTime\n      status\n      trackCondition\n      prizeMoney\n      fixedAvailable\n      starters\n      __typename\n    }\n    __typename\n  }\n}\n", "variables": {}}
    h = generate_hash(ts+'soonyinyin'+burp0_json["query"])
    burp0_url = "https://api.new.dynamicodds.com:443/query?ts={}&h={}".format(ts, h)
    r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
    res = r.json()
    ids = []
    for i in res['data']['meetingsDated']:
        source_id = i['externalIDs'][0]['id']
        for j in i['races']:
            now = now_utc = datetime.now(timezone.utc)
            now_8 = datetime.now(timezone.utc)+timedelta(minutes=8)
            MINUS_5 = datetime.now(timezone.utc)-timedelta(minutes=5)
            utc_then = datetime.strptime(j['startTime'], '%Y-%m-%dT%H:%M:%S%z')
            if utc_then > MINUS_5 and utc_then < now_8 and j['status'] == 'OPEN':
                ids.append((j['id'], source_id))
    print('[+] Found {} races | Less than 10 mins ,greater than -5m... status OPEN'.format(len(ids)))
    return ids


def get_id_n_type(_id, rno, token):

    burp0_url = "https://api.new.dynamicodds.com:443/public/GetDynamicRaceData?meeting_id={}&race_number={}".format(
        _id, rno)
    burp0_headers = {"Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"98\"", "Accept": "application/json, text/plain, */*",
                     "Authorization": token, "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://new.dynamicodds.com", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://new.dynamicodds.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    r = requests.get(burp0_url, headers=burp0_headers)
    res = r.json()
    try:
        return (res['do_meeting_id'], res['type'])
    except:
        return ("", "")

def get_bets(feed_data):
    race, token = feed_data
    rid, source_id = race
    ts = str(int(time.time()))
    burp0_headers = {"Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"98\"", "Accept": "*/*", "Content-Type": "application/json", "Authorization": token, "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
                     "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://new.dynamicodds.com", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://new.dynamicodds.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    burp0_json = {"operationName": None, "query": "{\n  race(id: \""+rid+"\") {\n    id\n    class\n    name\n    number\n    startTime\n    status\n    trackCondition\n    weather\n    distance\n    starters\n    prizeMoney\n    priceSets(\n      sources: [\"V\",\"CB2\",\"SB2\"]\n    ) {\n      source\n      meetingID\n      raceNumber\n      type\n      poolSize\n      updated\n      prices {\n        tabNo\n        price\n        __typename\n      }\n      __typename\n    }\n    competitors {\n      name\n      tabNo\n      scratchingType\n      runner {\n        id\n        __typename\n      }\n      __typename\n    }\n    meeting {\n      id\n      date\n      railPosition\n      externalIDs(sources: \"gbs\") {\n        id\n        __typename\n      }\n      track {\n        name\n        country\n        state\n        __typename\n      }\n      type\n      __typename\n    }\n    results(sources: []) {\n      status\n      source\n      positions {\n        tabNo\n        position\n        margin\n        __typename\n      }\n      dividends {\n        type\n        dividendNumbers\n        dividend\n        poolSize\n        status\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n", "variables": {}}
    h = generate_hash(ts+'soonyinyin'+burp0_json["query"])
    burp0_url = "https://api.new.dynamicodds.com:443/query?ts={}&h={}".format(
        ts, h)
    r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
    res = r.json()

    return_data = {}
    
    return_data['Updated_At'] = datetime.now(
        timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z')
    
    return_data['race_number'] = res['data']['race']['number']
    id_ntype = get_id_n_type(source_id, return_data['race_number'], token)
    try:
        return_data['ID'] = str(id_ntype[0])
    except:
        return ("","")
    return_data['Type'] = str(id_ntype[-1])
    return_data['title'] = res['data']['race']['meeting']['track']['name'] + \
        ' '+str(return_data['race_number'])
    tab_name_dict = {}
    SOURCE_REF = {
        'V': "VIC",
        'CB2': "PAYUP"
    }
    sb2_dict = {}
    for i in res['data']['race']['competitors']:
        tab_name_dict[str(i['tabNo'])] = {'name': i['name']}
        tab_name_dict[str(i['tabNo'])]['tabNo'] = str(i['tabNo'])

    for i in res['data']['race']['priceSets']:
        if 'WIN' in i['type']:
            source = i['source']
            if source == 'SB2':
                for j in i['prices']:
                    sb2_dict[str(j['tabNo'])] = str(j['price'])
                continue
            for j in i['prices']:
                tab_name_dict[str(j['tabNo'])][SOURCE_REF[source]] = str(
                    j['price'])
    f = open('race_bets.txt', 'a')
    f.write(r.text+'\n')
    f.close()
    for i in tab_name_dict:
        if 'PAYUP' not in tab_name_dict[i]:
            tab_name_dict[i]['PAYUP'] = '0'

        if tab_name_dict[i]['PAYUP'] == '0':
            if i in sb2_dict:
                tab_name_dict[i]['PAYUP'] = sb2_dict[i]
        print(tab_name_dict[i])

    return_data['odds'] = tab_name_dict
    return return_data


def upload_file():
    global ftp
    start = time.time()
    try:
        ftp.encoding = "utf-8"
        filename = "horse_new.xml"
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
        print("File Uploaded Successsfully....", convert_time(time.time()-start), ' seconds')

    except Exception as err:
        print('Retrying Login', err)
        try:
            ftp.quit()        
        except:
            pass
        ftp = FTP('racingbang.com', user='techypin@racingbang.com', passwd='P#1998iyush')


if __name__=="__main__":
    run()
