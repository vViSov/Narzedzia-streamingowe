from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
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
        with open(path, 'wb') as f:
            for data in r.iter_content(chunk_size=None):
                f.write(data)
        size = get_file_size(path, SIZE_UNIT.MB)
        elaps = round(time.time() - start, 1)
        print()
        print(f'> Pobrano plik: {path} | {round(size, 1)} MB | {elaps} Sek. | {l + 1} z {maksymalnaIlsocLinkow + 1} plików.')
    else:
        print('Nie udalo sie polaczyc z serwerem.')

print()

# Zmienne globalne ---->
pliki = []
nazwyPlikow = []
linkiPlikow = []

plikiWideoGotoweDoPobrania = []
rzeczywisteLinki = []

c = 0
k = 0
l = 0
# <----
options = Options()
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())

clearConsole()

print()

konto = input('> Czy chcesz sie zalogowac na swoje konto? <{Wymagane jeżeli chcesz pobrać prywatne pliki na swoim koncie}> (Tak/Nie): ')

print()

if konto == 'Tak' or konto == 'Yes' or konto == 'Y' or konto == 'tak' or konto == 'yes' or konto == 'y' or konto == 't':
    browser.get('https://cda.pl/login')

    clearConsole()

    print()
    login = input('> Podaj login lub adres e-mail do konta: ')
    print()
    password = input('> Podaj hasło do konta: ')
    print()

    browser.find_element(By.XPATH, '//*[@id="login"]').send_keys(login)
    browser.find_element(By.XPATH, '//*[@id="pass"]').send_keys(password)
    time.sleep(.3)
    browser.find_element(By.XPATH, '//*[@id="logowanieContainer"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/form/div[3]/div/div/button').click()
    
    clearConsole()
    print()
    print('> Zalogowano.')
    print()
elif konto == 'Nie' or konto == 'No' or konto == 'N' or konto == 'nie' or konto == 'no' or konto == 'n':
    clearConsole()
    print()
    print('> Nie zalogowano.')
    print()
else:
    clearConsole()
    print()
    print('> Nie zalogowano.')
    print()

browser.get('https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm?hl=pl')

time.sleep(2)

try:
    browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div').click()
except:
    print()
    print('> Wtyczka musi zostać dodana ręcznie.')
    print()

clearConsole()

print()
input('> Czy wtyczka zostala dodana? ')

clearConsole()
print()

folderDoPobrania = input('> Podaj link do folderu który chcesz pobrać: ')
browser.get(folderDoPobrania)

clearConsole()
print()

twojaNazwa = input('> Jezeli pliki sie nazywaja typu > {S01E01, S01E02} < dodaj nazwe serialu: ')
print()
nazwaFolderu = input('> Podaj nazwe folderu ktory utworzy program do zapisania plikow: ')

while True:
    clearConsole()
    if nazwaFolderu == '':
        print()
        print('> Musisz wprowadzić nazwę folderu.')
        print()
        nazwaFolderu = input('> Podaj nazwe folderu ktory utworzy program do zapisania plikow: ')
    else:
        print()
        print(f'> Utworzono folder o nazwie: "{nazwaFolderu}"')
        break


while True:
    print()
    print('> Zbieranie linkow oraz nazw plikow.')
    try:
        pliki = browser.find_elements(By.CLASS_NAME, 'link-title-visit')
        for iloscPlikow in range(len(pliki)):
            nazwyPlikow.append(pliki[iloscPlikow].get_attribute('text'))
            linkiPlikow.append(pliki[iloscPlikow].get_attribute('href'))
    except:
        print()
        print('> Nie znaleziono plikow video.')
        print()
    try:
        nastepnaPodstrona = browser.find_element(By.CLASS_NAME, 'next').get_attribute('href')
        browser.get(nastepnaPodstrona)
    except:
        print()
        print('> Brak kolejnej podstrony w folderze.')
        print()
        break

for maksymalnaIlsocLinkow in range(len(nazwyPlikow)):
    continue

print()
print()
print()


for linkiDoPobrania in range(len(linkiPlikow)):
    browser.get(linkiPlikow[linkiDoPobrania])
    
    clearConsole()

    print(f'> Plik {twojaNazwa + " " + nazwyPlikow[linkiDoPobrania]} > {linkiDoPobrania + 1} / {maksymalnaIlsocLinkow + 1}')
    print()

    try:
        browser.find_element(By.CLASS_NAME, 'pb-settings-click').click()
    except:
        print('> Wystąpił błąd.')

    try:
        wszystkieJakosci = browser.find_elements(By.CLASS_NAME, 'settings-quality')
    except:
        print('> Wystąpił błąd.')

    try:
        wszystkieJakosci[3].click()
        print(f'> Najwyższa jakosć to: 1080p.')
    except:
        try:
            wszystkieJakosci[2].click()
            print(f'> Najwyższa jakosć to: 720p.')
        except:
            try:
                wszystkieJakosci[1].click()
                print(f'> Najwyższa jakosć to: 480p.')
            except:
                try:
                    wszystkieJakosci[0].click()
                    print(f'> Najwyższa jakosć to: 360p.')
                except:
                    print('> Nie znaleziono odpowiedniej jakości.')

    time.sleep(1)
    
    plikiWideoGotoweDoPobrania.append((twojaNazwa + ' ' + nazwyPlikow[linkiDoPobrania] + '.mp4', browser.find_element(By.CLASS_NAME, 'pb-video-player').get_attribute('src')))

browser.quit()

clearConsole()

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
        print(f'> Utworzono folder o nazwe: "{nazwaFolderu}".')
        os.mkdir(nazwaFolderu)
        os.chdir(nazwaFolderu)
        break

clearConsole()

print()
print('> Rozpoczynam pobieranie plików...')
print()

results = ThreadPool(35).imap_unordered(download_file, plikiWideoGotoweDoPobrania)

for r in results:
    l += 1

print()
print('> Zakonczono pobieranie plikow.')
print()
