from itertools import count
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import shutil
from multiprocessing.pool import ThreadPool 
from time import time
import time
import os
import enum

clearConsole = lambda: os.system('cls')
clearConsole()

class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4

def get_file_size(file_name, size_type = SIZE_UNIT.BYTES ):
   """ Get file in size in given unit like KB, MB or GB"""
   size = os.path.getsize(file_name)
   return convert_unit(size, size_type)

def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == SIZE_UNIT.KB:
       return size_in_bytes/1024
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes/(1024*1024)
   elif unit == SIZE_UNIT.GB:
       return size_in_bytes/(1024*1024*1024)
   else:
       return size_in_bytes

def download_file(url):
    path, url = url
    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        start = time.time()
        try:
            with open(path, 'wb') as f:
                for data in r.iter_content(chunk_size=None):
                    f.write(data)
        except:
            while True:
                clearConsole()
                print(f'Plik {path} nie może się tak nazywać. ')
                path = input('Wprowadź własną nazwę dla tego pliku: ') + '.mp4'
                try:
                    with open(path, 'wb') as f:
                        for data in r.iter_content(chunk_size=None):
                            f.write(data)
                    break
                except:
                    continue

        size = get_file_size(path, SIZE_UNIT.MB)
        elaps = round(time.time() - start, 1)
        print()
        print(f'> Pobrano plik: {path} | {round(size, 1)} MB | {elaps} Sek. | {l + 1} z {grabberTimes + 1} plików.')
    else:
        print('Nie udalo sie polaczyc z serwerem.')

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    browser.get('https://chrome.google.com/webstore/detail/adguard-adblocker/bgnkhhnnamicmpeenaelnjfhikgbkllg?hl=pl')

    time.sleep(1.5)

    browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div').click()
except:
    print('Wtyczka musi zostac dodana recznie.')

input('Czy wtyczka zostala dodana?')
clearConsole()

try:
    browser.get('https://chrome.google.com/webstore/detail/hcaptcha-solver/lfpfbgeoodeejmjdlfjbfjkemjlblijg')

    time.sleep(1.5)

    browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div').click()
except:
    print('Wtyczka musi zostac dodana recznie.')

input('Czy wtyczka zostala dodana?')
clearConsole()

try:
    browser.get('https://chrome.google.com/webstore/detail/stay-secure-with-cybergho/ffbkglfijbcbgblgflchnbphjdllaogb')

    time.sleep(1.5)

    browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div').click()
except:
    print('Wtyczka musi zostac dodana recznie.')

input('Czy wtyczka zostala dodana?')
clearConsole()

urlsListDownload = []
nazwaSerialu = []
linkSerialu = []
urlsToDownload = ''
grabbedRealUrlsList = []
grabbedRealUrlsStr = ''
realUrls = []
namesLook = ''
namesShow = []
l = 0

clearConsole = lambda: os.system('cls')
clearConsole()

URL = input('> Wprowadz link do zeriona ktory prowadzi do calego serialu: ')

nazwaFolderu = input('> Wprowadz nazwe folderu ktory ma utworzyc program do zapisania w nim plikow: ')

while True:
    clearConsole()
    if os.path.exists(nazwaFolderu):
        print(f'> Folder z nazwą "{nazwaFolderu}" już istnieje!')
        print()
        nazwaFolderu = input('Wprowadź nazwę inną folderu: ')
        continue
    else:
        clearConsole()
        print()
        try:
            os.mkdir(nazwaFolderu)
            os.chdir(nazwaFolderu)
            print(f'> Utworzono folder o nazwe: "{nazwaFolderu}".')
            break
        except:
            nazwaFolderu = input('> Folder nie moze byc tak nazwany, wprowadź inną nazwę folderu: ')

clearConsole()

browser.get(URL)

serial = browser.find_elements(By.CLASS_NAME, 'preview')

nazwaDiv = browser.find_elements(By.CLASS_NAME, 'title-date-block')
nazwa = browser.find_elements(By.CLASS_NAME, 'title')
linkA = browser.find_elements(By.TAG_NAME, 'a')

nazwa.pop(0)
print()
print()

for nazwaCount in range(len(nazwaDiv)):
    clearConsole()

for seriale in range(len(serial)):
    nazwaSerialu.append(nazwa[seriale].get_attribute('innerText'))
    linkSerialu.append(serial[seriale].get_attribute('href'))
    clearConsole()

print()
print()

for clickCounts in range(len(linkSerialu)):
    URL = linkSerialu[clickCounts]
    browser.get(URL)
    
    time.sleep(.5)

    try:
        try:
            el1 = browser.find_element(By.XPATH, '//*[@id="episode-page"]/div/div[1]/div[2]/table/tbody/tr[1]')
            el2 = browser.find_element(By.XPATH, '//*[@id="episode-page"]/div/div[1]/div[2]/table/tbody/tr[2]')
            el3 = browser.find_element(By.XPATH, '//*[@id="episode-page"]/div/div[1]/div[2]/table/tbody/tr[3]')
            el4 = browser.find_element(By.XPATH, '//*[@id="episode-page"]/div/div[1]/div[2]/table/tbody/tr[4]')
        except:
            print('Nie odnaleziono elementu HTML.')

        if 'highload' in el1.get_attribute('innerHTML'):
            browser.find_element(By.XPATH, '//*[@id="episode-page"]/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/div').click()

        elif 'highload' in el2.get_attribute('innerHTML'):
            browser.find_element(By.XPATH, '//*[@id="episode-page"]/div/div[1]/div[2]/table/tbody/tr[2]/td[3]/div').click()

        elif 'highload' in el3.get_attribute('innerHTML'):
            browser.find_element(By.XPATH, '//*[@id="episode-page"]/div/div[1]/div[2]/table/tbody/tr[3]/td[3]/div').click()
        
        elif 'highload' in el3.get_attribute('innerHTML'):
            browser.find_element(By.XPATH, '//*[@id="episode-page"]/div/div[1]/div[2]/table/tbody/tr[4]/td[3]/div').click()
        else:
            print('> Otrzymano linki.')
            break
    except:
        print('> Nie odnaleziono elementu HTML.')
    
    time.sleep(1)

    playerCaptcha = browser.find_element(By.CLASS_NAME, 'player-captcha').get_attribute('style')

    if playerCaptcha == 'display: flex;':
        print()
        print('- - - - ' * 3)
        print('> Łamanie hCaptcha...')
        print('- - - - ' * 3)
        print()
        while playerCaptcha == 'display: flex;':
            playerCaptcha = browser.find_element(By.CLASS_NAME, 'player-captcha').get_attribute('style')
            time.sleep(2)
        
        print()
        print('- - - - ' * 3)
        print('> hCaptcha zostało Złamane...')
        print('- - - - ' * 3)
        print()
        srcUrl = browser.find_element(By.ID, 'pframe')
        urlsToDownload += srcUrl.get_attribute('src') + ' ' + '\n'
        urlsListDownload.append(srcUrl.get_attribute('src'))
    else:
        srcUrl = browser.find_element(By.ID, 'pframe')
        urlsToDownload += srcUrl.get_attribute('src') + ' ' + '\n'
        urlsListDownload.append(srcUrl.get_attribute('src'))
    
    time.sleep(2)

    if clickCounts % 6 == 0:
        print()
        print('> Nie zapomnij o VPN!')
        print()
        print()

    print(f'> Łamanie hCaptcha nie jest wymagane: {clickCounts + 1}: {srcUrl.get_attribute("src")}')

    listOfWhatUrl = urlsListDownload[clickCounts][slice(20)]

    print()

    if 'https://highload.to/' in listOfWhatUrl:
        realUrls.append(urlsListDownload[clickCounts])
        namesLook += nazwaSerialu[clickCounts] + ' -> ' + urlsListDownload[clickCounts] + ' ' + '\n'
        namesShow.append(nazwaSerialu[clickCounts])

for showCounts in range(len(nazwa)):
    print(f'Serial: {nazwaSerialu[showCounts]} -> {urlsListDownload[showCounts]}')
print(f'Znaleziono odcinków: {nazwaCount + 1}')

for grabberTimes in range(len(urlsListDownload)):
    try:
        browser.get(realUrls[grabberTimes])
        grabbedUrl = browser.find_element(By.XPATH, '//*[@id="faststream_html5_api"]').get_attribute('src')
        grabbedRealUrlsList.append((nazwaSerialu[grabberTimes] + '.mp4', grabbedUrl))
        grabbedRealUrlsStr += grabbedUrl + ' ' + '\n'
        time.sleep(1.5)
    except:
        print()
        print(f'> Plku wideo nie odnaleziono: {urlsListDownload[grabberTimes]}')
        print()
        continue

browser.quit()

clearConsole()

req = ThreadPool(50).imap_unordered(download_file, grabbedRealUrlsList)

for x in req:
    l += 1

print(f'Ilosc niedostepnych plikow: {l + 1 - grabberTimes + 1}')

print('Pobrano wszystkie pliki.')
