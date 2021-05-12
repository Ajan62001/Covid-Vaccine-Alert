# Python script for Amazon product availability checker
# importing libraries
import requests
from time import sleep
import time
import schedule
import smtplib


def check(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
	
	# adding headers to show that you are
	# a browser who is sending GET request
	page = requests.get(url, headers = headers)
	for i in range(200):
		sleep(3)
		AVAIL = []

		p = page.json()
		for center in p['sessions']:
			if center['available_capacity'] >=1 and center['min_age_limit']==18:
					AVAIL.append("Vaccine H ABHI " +str( center['min_age_limit'] )+ " +Ke LIYe "+str(center["date"])) 
		return AVAIL

	
def sendemail(ans):
	GMAIL_USERNAME = ""
	GMAIL_PASSWORD = ""
	
	recipients = []
	body_of_email = "Vaccine Check  \n"+str(ans)
	print(ans)
	# for a in ans:
	# 	body_of_email+=(a+"\n")
	email_subject = ' Vaccine availability'
	
	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)
	
	# start TLS for security
	s.starttls()
	
	# Authentication
	s.login(GMAIL_USERNAME, GMAIL_PASSWORD)
	
	# message to be sent
	
	for recipient in recipients:
		headers = "\r\n".join(["from: " + GMAIL_USERNAME,
						"subject: " + email_subject,
						"to: " + recipient,
						"mime-version: 1.0",
						"content-type: text/html"])
		content = headers + "\r\n\r\n" + body_of_email

		s.sendmail(GMAIL_USERNAME, recipient, content)

	s.quit()


def ReadAsin():
	# Asin Id is the product Id which
	# needs to be provided by the user
	pin = ""
	dates = ["12-05-2021","13-05-2021","14-05-2021"]
	for date in dates:
		url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+pin+"&date="+date
		print ("Processing: "+url)
		ans = check(url)
		if len(ans)>0:
			sendemail(ans)

def job():
	print("Tracking....")
	ReadAsin()
print("Process >>>>>>>>>")
schedule.every(2).minutes.do(job)

while True:
	
	# running all pending tasks/jobs
	schedule.run_pending()
	time.sleep(300)
