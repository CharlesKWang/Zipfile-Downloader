# Zipfile-Downloader
Finds and downloads zip files from the NYC Open Data Page from within the NYCDoHMH network.

# Prerequisites
dependancies include the requests, beautifulsoup, zipfile, io, sys, os, and configparser libraries.

# Setup
The settings.ini file must be modified to your specifications. It contains the following four fields:
ExtractFlag - Set to either "True" or "False", determines whether you wish to download the extracted zips, or the compressed.
DownloadFolder - The location you wish to download to. Ex: "C:/User/Downloads"

User - Your network username
Pass - Your network password

If you're not running this from within the Department of Health network, you may ignore the username and password settings. These were only necessary to pass network security protocols. Within the script itself, you should configure the proxy settings to your local network. 

# Running
The program is a basic web scraper for NYC publicly available data. Running the script will search a few select pages for zip files, and automatically download them to a specified directory.

# To Do
If I've got time, I have some ideas of things to do with the public data for other personal projects, so I may update this to be more flexible and less DoHMH specific.
