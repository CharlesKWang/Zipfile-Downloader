#******************************************************************************
# Affiliation: NYCDoHMH
# Title: Zip Files
# Author: Charles Wang
# 
# About: Finds and downloads zip files from NYC Open Data Pages 
#
#******************************************************************************
import requests
from bs4 import BeautifulSoup
import zipfile
import io
import sys
import os
import configparser

def directory_exists(dpath):
    """Function to check if a directory exists, and if not create it"""
    d = os.path.dirname(dpath)
    if not os.path.exists(d):
        os.makedirs(d)
        
baseUrl = 'http://www1.nyc.gov'

#Looks for settings file
local_path = sys.path[0]
settings_file = os.path.join(local_path, "settings.ini")                
if os.path.isfile(settings_file):
    config = configparser.ConfigParser()
    config.read(settings_file)
else:
    print("INI file not found. \nMake sure a valid 'settings.ini' file exists in the same directory as this script.")
    sys.exit()
    
username = config.get('ACCOUNT', 'USER')
password = config.get('ACCOUNT', 'PASS')
extract_flag = config.get('FILE', 'EXTRACTFLAG')
download_path = config.get('FILE', 'DOWNLOADFOLDER')

proxyDict = {'http' : 'http://health%5C{}:{}@healthproxy.health.dohmh.nycnet:8080'.format(username, password),
             'https' : 'http://health%5C{}:{}@healthproxy.health.dohmh.nycnet:8080'.format(username, password),
             'ftp' : 'http://health%5C{}:{}@healthproxy.health.dohmh.nycnet:8080'.format(username, password),
             }

dataUrl = "http://www1.nyc.gov/site/planning/data-maps/open-data.page"
r = requests.get(dataUrl, proxies=proxyDict)
soup = BeautifulSoup(r.content)
links = soup.find_all('a', href=True)
zipUrls = []

#Include the pluto page directly, to avoid the authentication redirect
#Include the districts page directly, as it's named differently
referPages = ["/site/planning/data-maps/open-data/dwn-pluto-mappluto.page",
              "/site/planning/data-maps/open-data/districts-download-metadata.page"]
for link in links:
    if 'open-data/dwn' in link['href'] and link['href'] not in referPages:
        if '#' not in link['href']:
            referPages.append(link['href'])

for link in links:
    if '/download/zip' in link['href']:
        filename = link['href']
        zipUrls.append(baseUrl + filename)
    
                  
for page in referPages:
    r = requests.get(baseUrl + page, proxies=proxyDict)
    soup = BeautifulSoup(r.content)
    
    referLinks = soup.find_all('a', href=True)
    for link in referLinks:
        if '/download/zip' in link['href']:
            filename = link['href']
            zipUrls.append(baseUrl + filename)
            
#DOITT Pages                
url = "http://cityshare.nycnet/html/gis/html/downloads/downloads.shtml"
r = requests.get(url, proxies=proxyDict)
soup = BeautifulSoup(r.content)
links = soup.find_all('a', href=True)

for link in links:
    if 'cscl/' in link['href']:
        filename = link['href'].split('/')[-1]
        zipUrls.append(link['href'])
        print (filename)

zipUrls = list(set(zipUrls))
print (zipUrls)

for zipFile in zipUrls:
    filename = zipFile.split('/')[-1].strip('?r=1')
    print (filename)    
    localPath = download_path
    FilePath = os.path.join(localPath, filename)
    r = requests.get(zipFile, proxies=proxyDict, stream=True)
    
    #Extract Contents
    if extract_flag == 'True':
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(localPath + filename.strip('.zip') + '/' )
        z.close()
    
    #Save as Zip
    elif extract_flag == 'False':
        with open(FilePath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        print("Specify a valid ExtractFlag value (True or False)")