#importing required libraries
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pymysql.cursors
import pandas as pd

#link of the page to start scraping from
link = str(input("Please enter the link of the category to be scraped (with / at the end): "))
#corresponding page number
page_number = int(input('Please enter page number: '))

#create empty dataframe with column names, data will be saved later
#df = pd.DataFrame(columns=['author','Title','date','content'])

def scrape_one_page(input_link):
	# List of scraped usernames
	usernames = []
	# List of scraped post titles
	post_title = []
	# List of scraped post content
	post_content = []
	# List of scraped date for each post
	corresponding_date = []


	# The link to the post, to be used inside the script.
	corresponding_thread_link = []


	# Loggining in the forum and performing the scraping operation
	with sync_playwright() as p:
		#launching browser
		browser = p.chromium.launch(headless = True, slow_mo = 50)
		page = browser.new_page()
		#select login page
		page.goto('https://xss.is')


		#filling login credentials and submitting to server
		#Enter login credentials here
		#################################################
		page.fill('input[name="login"]','username_enter_here')
		page.fill('input[name="password"]','passwrod_enter_here')
		#################################################

		
		page.click("text=Войти", delay=100)
		#Fetching the selected  category
		page.goto(input_link)
		#Extracting all html content for BeautifulSoup
		html = page.inner_html('#XF')
		#Injecting content into BS4 parser
		soup = BeautifulSoup(html,'html.parser')

		max_pages = soup.find_all('input',class_='input input--numberNarrow js-pageJumpPage')
		print(max_pages)
		#ultag is the ul html tag, same for atag
		#The first loop will go over the ul tags and extract all the a and li tags
		for ultag in soup.find_all('ul', {'class': 'structItem-parts'}):
			#First, extracting usernames
			for atag in ultag.find_all('a', class_='username'):
				usernames.append(atag.get_text())
			#Second, extracting date and saving it to the corresponding_date list
			for litag in ultag.find_all('li',class_='structItem-startDate'):
				thread = litag.find('a')['href']
				date = litag.find('time')['data-date-string']
				time = litag.find('time')['data-time-string']
				corresponding_date.append((date,time))
				corresponding_thread_link.append(thread)

		#We use the saved thread links to scrape the post content and save it.
		#The loop will go over each link. inject it in the bs4 and extract the required information
		for thread in corresponding_thread_link:
			link = 'https://xss.is'+str(thread)
			page.goto(link)
			#The XF is the html id to get all the html content in the page
			content = page.inner_html('#XF')
			soup = BeautifulSoup(content,'html.parser')
			#We use the title keyword to locate it
			title = soup.find('title').get_text()
			post_title.append(title)
			#The post content is located uder <article> tag.
			post = soup.find('article',class_='message-body js-selectToQuote').get_text()
			post_content.append(post)

	print('Data scraped successfully.')		
	#update the dataframe initiliazed above
	#save the dataframe in csv file
	#df.to_csv('scraped.csv')
	print("Writing data to MySql database")
	connection = pymysql.connect(host='localhost', 
                             user='root', 
                             password='', 
                             db='xss.is', 
                             cursorclass=pymysql.cursors.DictCursor) 
 
	with connection.cursor() as cursor: 
		for i in range(len(usernames)):
			sql = "INSERT INTO `posts` (`author`, `title`,`date`,`content`) VALUES (%r, %r, %r, %r)" 
			cursor.execute(sql, (usernames[i], post_title[i],corresponding_date[i],post_content[i])) 
			connection.commit() 

links = []
for i in range(page_number,200):
	links.append(str(link)+'page-'+str(i))

counter = page_number
for link in links:
	scrape_one_page(link)
	print('Page number: '+str(counter)+' scraped successfully.')
	counter+=1



