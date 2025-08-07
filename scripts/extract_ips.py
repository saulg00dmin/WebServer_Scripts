import pandas as pd
import os
import re
from datetime import datetime

# File paths
EXCEL_DIR = "/opt/malicious_ips_data/"
OUTPUT_FILE = "/var/www/html/malicious_ips.txt"
DATE_TRACK_FILE = "/var/www/html/malicious_ips_dates.txt"

def load_existing_ips():
    """Load existing IPs from both malicious_ips.txt and malicious_ips_dates.txt."""
    existing_ips = set()

    # Load from malicious_ips.txt
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            existing_ips.update(line.strip() for line in f if line.strip())

    # Load from malicious_ips_dates.txt
    if os.path.exists(DATE_TRACK_FILE):
        with open(DATE_TRACK_FILE, "r") as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    existing_ips.add(parts[0])  # Only store the IP, ignore timestamp

    return existing_ips

def extract_ips():
    """Extracts unique IPs across all Excel files and ensures no duplicates."""
    existing_ips = load_existing_ips()
    ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    new_ips = set()
    timestamp = datetime.now().strftime("%Y-%m-%d")

    # Remove immutable flags before modifying files
    os.system(f"sudo chattr -i {OUTPUT_FILE}")
    os.system(f"sudo chattr -i {DATE_TRACK_FILE}")

    # Collect unique IPs from all Excel files
    extracted_ips = set()
    for file in os.listdir(EXCEL_DIR):
        if file.endswith(".xlsx"):
            file_path = os.path.join(EXCEL_DIR, file)
            try:
                xls = pd.ExcelFile(file_path)
                sheet_name = ' IPs'
                if sheet_name in xls.sheet_names:
                    df_ips = pd.read_excel(xls, sheet_name=sheet_name)
                    raw_ips = df_ips.iloc[1:, 0].dropna()
                    cleaned_ips = {ip.strip().split()[0] for ip in raw_ips.astype(str) if ip_pattern.match(ip.strip().split()[0])}

                    extracted_ips.update(cleaned_ips)  # Store all unique IPs found

            except Exception as e:
                print(f"Error processing {file}: {e}")

    # Filter out already existing IPs
    new_ips = extracted_ips - existing_ips  # Only truly new IPs

    if new_ips:
        print(f"Writing {len(new_ips)} new IPs to {OUTPUT_FILE}")

        # Append only unique new IPs
        with open(OUTPUT_FILE, "a") as f:
            f.write("\n".join(new_ips) + "\n")

        print(f"Writing {len(new_ips)} timestamps to {DATE_TRACK_FILE}")

        # Append only unique new timestamps
        with open(DATE_TRACK_FILE, "a") as f:
            for ip in new_ips:
                f.write(f"{ip} {timestamp}\n")

    # Reapply immutable flags
    os.system(f"sudo chattr +i {OUTPUT_FILE}")
    os.system(f"sudo chattr +i {DATE_TRACK_FILE}")

    print(f"Added {len(new_ips)} new IPs.")

if __name__ == "__main__":
    extract_ips()
