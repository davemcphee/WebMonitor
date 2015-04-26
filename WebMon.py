# Monitors a webpage for changes
# For each URL, creates a hash of URL, then writes hash of contents to WebMon.shelve
# uses built-in hashlib lib, md5 digest (who cares about sec we only need a digest
# always use hash.hexdigest for portability

# open shelve file that contains list of URLs to monitor, with current md5 hash
# alert by sending SMS via email : cellnumber@tmomail.net for tmobile. Google for alt. carriers.
# 
# need to have an existing shelve file in current dir obv

# v0.1 04/24/2015


import hashlib, requests, os, shelve, sys, smtplib, configparser

#bunch of bs about finding path, so 
pathname = os.path.dirname(sys.argv[0]) 

shelveFile = ''.join([os.path.abspath(pathname), '\conf\WebMon.shelve'])
s = shelve.open(shelveFile, writeback=True)

configfile = ''.join([os.path.abspath(pathname), '\conf\WebMon.config'])
config = configparser.ConfigParser()
config.read(configfile)

session = requests.Session()

def sendAlert(url):
	# need to setup WebMon.config first
	msg = 'Subject: WebMon.py update\n\n%s' % (url)
	server = smtplib.SMTP_SSL('smtp.gmail.com:465')
	server.login(config['WebMon']['username'], config['WebMon']['password'])
	server.sendmail(config['WebMon']['fromaddr'], config['WebMon']['toaddr'], msg)
	server.quit()


for url in s:
	knownHash = s[url]
	print("Checking", url, "for any changes..")
	r = session.get(url)
	if (r.status_code != 200):
		print('Unable to retrieve', url, '\nGot error code', r.status_code, 'exiting\n')
		sys.exit()
	newHash = hashlib.md5(bytes(r.text, 'utf-8')).hexdigest()
	if newHash != knownHash:		# URL has changed
		print(url, ' has changed!')
		s[url] = newHash	#update shelf
		sendAlert(url)


		
s.close()
print("Done.\n\n")
		