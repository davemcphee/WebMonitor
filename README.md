# WebMonitor
Quick script to monitor web pages for changes. Only monitors html. 

WebMon stores an MD5 hash of the html in a python shelve file, and maintains a list of URLs to monitor in the conf\WebMon.config file

Run without params (eg.: from the Windows scheduler), it will iterate thought the list of URLs, generate a hash, and compare to stored hash. If the two are different, it will send an alert - currently an email, although you can use the email functionality to send an SMS, see this for a list of carriers that support this: http://www.textsendr.com/emailsms.php

#ToDo
* implement -init command, which will add a new URL to config, and update shelve with HASH without alerting. 
