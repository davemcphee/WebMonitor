# Monitors a webpage for changes
# For each URL, creates a hash of URL, then writes hash of contents to WebMon.shelve
# uses built-in hashlib lib, md5 digest (who cares about sec we only need a digest
# always use hash.hexdigest for portability

# open shelve file that contains list of URLs to monitor, with current md5 hash
# alert by sending SMS via email : cellnumber@tmomail.net for tmobile. Google for alt. carriers.
# 
# need to have an existing shelve file in current dir obv

# v0.1 04/24/2015


import hashlib, requests, os, sys, smtplib, configparser, argparse

#bunch of bs about finding path, to help load config file from anywhere
pathname = os.path.dirname(sys.argv[0]) 
configfile = ''.join([os.path.abspath(pathname), '\conf\WebMon.config'])
config = configparser.ConfigParser(delimiters='|')
config.read(configfile)

session = requests.Session()

def sendAlert(url):
	# need to setup WebMon.config first
	msg = 'Subject: WebMon.py update\n\n%s' % (url)
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com:465')
		server.login(config['WebMon']['username'], config['WebMon']['password'])
		server.sendmail(config['WebMon']['fromaddr'], config['WebMon']['toaddr'], msg)
		server.quit()
	except SMTPException:
		print('Got an error trying to send email!')
		return 0
	return 1

def monitor():
	for url in config['URLs']:
		knownHash = config['URLs'][url]
		print("Checking", url, "for any changes..")
		r = session.get(url)
		if (r.status_code != 200):
			print('Unable to retrieve', url, '\nGot error code', r.status_code, 'exiting\n')
			sys.exit()
		newHash = hashlib.md5(bytes(r.text, 'utf-8')).hexdigest()
		if newHash != knownHash:		# URL has changed
			print(url, ' has changed!')
			if sendAlert(url):			#if alert is successfully sent, update. Don't update if failure!
					config['URLs'][url] = newHash
					with open(configfile, 'w') as outfile:
						config.write(outfile)
		else:
			print("none detected")
			

def init(url):
	r = session.get(url)
	if (r.status_code != 200):
		print('Unable to retrieve', url, '\nGot error code', r.status_code, 'exiting\n')
		sys.exit()	
	
	print('Sucesfully retrieved', url, '\nAdding to known list')
	newHash = hashlib.md5(bytes(r.text, 'utf-8')).hexdigest()
	config['URLs'][url] = newHash
	with open(configfile, 'w') as outfile:
		config.write(outfile)
	


def main():
	parser = argparse.ArgumentParser(description='A script that monitors a list of known URLs')
	parser.add_argument("--init", help="Add a new URL and hash to our list of knowns")
	args = parser.parse_args()
	
	if args.init:
		init(args.init)
	else:
		monitor()
		
	
	# if init argument given, run init and exit
	# otherwise, run monitor and exit
	

if __name__ == "__main__" :
		main()