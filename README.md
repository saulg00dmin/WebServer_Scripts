<h2>Scripts for Maintaining a Threat Feed Web Server</h2>

<h3>Available Scripts</h3>

<p><code>extract_ips.py</code>  
Extracts all IP addresses from an Excel spreadsheet and writes only the unique entries to <code>malicious_ips.txt</code> in the Linux web root directory (<code>/var/www/html</code>).  
This file can then be used to provide an IDS/IPS with an updated threat feed.</p>

<p><code>trim_malicious_ips.sh</code>  
Removes any IP addresses older than 30 days from the <code>malicious_ips.txt</code> file in <code>/var/www/html</code>, ensuring the list remains current.</p>
