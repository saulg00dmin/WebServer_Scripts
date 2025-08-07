#!/bin/bash

# Define file paths
IP_FILE="/var/www/html/malicious_ips.txt"
DATE_FILE="/var/www/html/malicious_ips_dates.txt"
TEMP_IP_FILE="/var/www/html/temp_malicious_ips.txt"
TEMP_DATE_FILE="/var/www/html/temp_malicious_ips_dates.txt"
LOG_FILE="/var/www/html/malicious_ip_cleanup.log"

# Get current date in Unix timestamp
CURRENT_DATE=$(date +%s)
EXPIRATION_SECONDS=$((30 * 24 * 60 * 60)) # 30 days

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Ensure logging file exists
if ! [ -f "$LOG_FILE" ]; then sudo touch "$LOG_FILE"; fi

# Check and remove immutable flag only if necessary
if lsattr "$IP_FILE" | grep -q "i"; then
    sudo chattr -i "$IP_FILE" "$DATE_FILE"
    log_message "Removed immutable flag from files."
fi

# Create empty temp files
> "$TEMP_IP_FILE"
> "$TEMP_DATE_FILE"

# Trap to clean up temp files on exit or failure
trap 'rm -f "$TEMP_IP_FILE" "$TEMP_DATE_FILE"; exit' INT TERM EXIT

# Process and filter IPs using awk for efficiency
awk -v current="$CURRENT_DATE" -v expire="$EXPIRATION_SECONDS" '
{
    cmd = "date -d " $2 " +%s 2>/dev/null";
    cmd | getline timestamp;
    close(cmd);
    
    if (timestamp != "" && (current - timestamp) <= expire) {
        print $1 >> "'$TEMP_IP_FILE'"
        print $1, $2 >> "'$TEMP_DATE_FILE'"
    }
}' "$DATE_FILE"

# Ensure temp files are not empty before replacing
if [ -s "$TEMP_IP_FILE" ] && [ -s "$TEMP_DATE_FILE" ]; then
    mv -f "$TEMP_IP_FILE" "$IP_FILE"
    mv -f "$TEMP_DATE_FILE" "$DATE_FILE"
    log_message "Updated malicious IP list. Expired entries removed."
else
    log_message "No valid IPs remaining. Keeping existing files."
    rm -f "$TEMP_IP_FILE" "$TEMP_DATE_FILE"
fi

# Reapply immutable flag
sudo chattr +i "$IP_FILE" "$DATE_FILE"
log_message "Reapplied immutable flag to files."

log_message "Cleanup complete."

# Remove trap and exit successfully
trap - INT TERM EXIT
exit 0
