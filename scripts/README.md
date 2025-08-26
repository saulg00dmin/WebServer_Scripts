<h2> Directions for extract_ips.py </h2>

<h3>Prerequesites</h3>

Create the following empty files and directories. You can updaate the sript to make them for you if you like or update the script to do so.
``` bash
/opt/malicious_ips_data/
```
```bash
/var/www/html/malicious_ips.txt
```
``` bash
/var/www/html/malicious_ips_dates.txt
```

1. Create the empty files and folder per the prerequsites,
2. Download an excel .xlsx file and place it into the `/opt/malicious_ips_data` folder.
3. Run the `extract_ips.py` script via `python3 extract_ips.py`

The script with create a running list of ips with a time stamps in a seperate file on you webserver to feed into an IPS/IDS.
The second script will trime any IPs older than 30 days. You can run the in a cron like I do.



