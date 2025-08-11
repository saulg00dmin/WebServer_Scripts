Populating a threat feed web server

Scripts: 
extract_ips.py - extract's all ip's from an excel spreadsheet and adds all the unique ones to a file called malicious_ips.txt and places it in /var/www/html to use in workbook or feed into IDS/IPS.
trim_malicious_ips.sh - trims and removed IPs older than 30 days from the malicious_ips.txt file in /var/www/html.
