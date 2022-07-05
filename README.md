# Scripts
I will upload here different python scripts for scraping and automation. Feel free to use them at your own risk!
## Table of contents
* [XSS script](#xss-script)
## XSS script
This is a python based script to scrape content from the russian hacking forum XSS.IS. The script crawls the different sections of the forum and downloads
all the corresponding pages. The scraped data consists of author name, posting date, post title and content. Later, the data is saved into a MySQL database
for further usage. When applying some changes, the script could be used for other similar forums. The libraries used for this work are BeautifulSoup, 
Playwright and Pandas. To make the script work, you need to update the login section with your own login credentials. When trying to make changes, you will
find comments above each line so that it's easier to update the script.
