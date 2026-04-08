import os
import sys
import json
import time
import logging
import requests
import urllib3
import pyodbc
import csv
import zipfile
import io
from datetime import datetime, UTC, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Paths ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
LOG_PATH = os.path.join(BASE_DIR, "greenwallbox.log")

#--- Logging ---
# The code snippet you provided is configuring the logging module in Python. Here's what each part of
# the code does:
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger()

# --- Config ---
def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)

# --- MSSQL ---
def connect_db(cfg):
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={cfg['sql_server']};"
        f"DATABASE={cfg['sql_database']};"
        f"UID={cfg['sql_user']};"
        f"PWD={cfg['sql_password']};"
        f"TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

# --- Login ---
def login(cfg):
    logger.info("Attempting to log in to GreenWallbox API...")
    resp = requests.post(cfg["api_login_url"], json={
        "login": cfg["username"],
        "password": cfg["password"]
    }, verify=False)

    if resp.status_code != 200:
        raise Exception(f"Login failed: {resp.status_code} - {resp.text}")

    token = resp.json().get("token")
    if not token:
        raise Exception("No token returned from API.")
    logger.info("Login successful.")
    return token

# --- Report Download ---
def download_report(cfg, token, start_date, end_date):
    logger.info(f"Downloading report from {start_date} to {end_date}...")
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    params = {
        "ObjectsIds": cfg["object_ids"],
        "TimeBegin": f"{start_date} 00:00:00Z",
        "TimeEnd": f"{end_date} 23:59:59Z",
        "Lang": "PL",
        "TimeFormat": "Local",
        "FileNamePrefix": "Charging_sessions"
    }

    resp = requests.get(cfg["api_export_url"], headers=headers, params=params, verify=False)

    if resp.status_code == 200 and resp.content:
        logger.info("Report successfully downloaded.")
        return resp.content
    elif resp.status_code == 204:
        logger.warning("No data returned (204).")
        return None
    else:
        raise Exception(f"Download failed: {resp.status_code} - {resp.text}")

# --- Extract CSV from ZIP ---
def extract_csv_from_zip(zip_data: bytes) -> bytes:
    try:
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            # Znajdź pierwszy plik CSV w archiwum
            csv_files = [name for name in z.namelist() if name.lower().endswith('.csv')]
            if not csv_files:
                raise Exception("No CSV file found in ZIP archive.")
            
            csv_filename = csv_files[0]
            logger.info(f"Extracting CSV file: {csv_filename}")
            return z.read(csv_filename)
    except zipfile.BadZipFile:
        raise Exception("Downloaded file is not a valid ZIP archive.")

# --- CSV Decode ---
def decode_csv_bytes(data: bytes) -> str:
    try:
        # Najpierw próbuj UTF-8 with BOM
        text = data.decode('utf-8-sig')
        logger.info("CSV decoded successfully using utf-8-sig (UTF-8 with BOM).")
        return text
    except UnicodeDecodeError:
        # Jeśli nie zadziała, spróbuj innych kodowań
        for enc in ["utf-8", "cp1250", "latin1"]:
            try:
                text = data.decode(enc)
                logger.info(f"CSV decoded successfully using {enc}.")
                return text
            except UnicodeDecodeError:
                continue
        raise Exception("Unable to decode CSV file with standard encodings.")

# --- Save Report to DB ---
def save_to_db(cfg, zip_data):
    conn = connect_db(cfg)
    cursor = conn.cursor()

    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='GreenWallbox' AND xtype='U')
        CREATE TABLE GreenWallbox (
            [UserName] NVARCHAR(255),
            [StartDate] NVARCHAR(255),
            [StartHour] NVARCHAR(255),
            [EndDate] NVARCHAR(255),
            [EndHour] NVARCHAR(255),
            [ChargingTime] NVARCHAR(255),
            [Energy] FLOAT
        )
    """)
    conn.commit()

    # unzip and decode CSV data
    csv_data = extract_csv_from_zip(zip_data)
    
    text = decode_csv_bytes(csv_data).strip()
    # Detect delimiter automatically
    delimiter = ';' if text.count(';') > text.count(',') else ','

    reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    headers = reader.fieldnames
    logger.info(f"Detected CSV headers: {headers}")
    
    energy_col = None
    username_col = None
    startdate_col = None
    starthour_col = None
    enddate_col = None
    endhour_col = None
    chartime_col = None
    
    for h in headers:
        h_lower = h.lower()
        if "dostarczona energia" in h_lower or "energia" in h_lower and "kwh" in h_lower:
            energy_col = h
        elif "data startu" in h_lower or ("data" in h_lower and "start" in h_lower):
            startdate_col = h
        elif "godzina startu" in h_lower or ("godzina" in h_lower and "start" in h_lower):
            starthour_col = h
        elif "data zakończenia" in h_lower or ("data" in h_lower and "zako" in h_lower):
            enddate_col = h
        elif "godzina zakończenia" in h_lower or ("godzina" in h_lower and "zako" in h_lower):
            endhour_col = h
        elif "czas trwania" in h_lower or ("czas" in h_lower and "trwania" in h_lower):
            chartime_col = h
        elif "nazwa uzytkownika" in h_lower or "użytkownik" in h_lower:
            username_col = h
        

    if not all([energy_col, username_col, startdate_col, starthour_col, enddate_col, endhour_col, chartime_col]):
        logger.error("CSV columns not recognized. Check header names.")
        logger.error(f"Found: Energy={energy_col}, UserName={username_col}, StartDate={startdate_col}, StartHour={starthour_col}, EndDate={enddate_col}, EndHour={endhour_col}, ChargingTime={chartime_col}")
        logger.error(f"Available headers: {headers}")
        return

    logger.info(f"Mapped columns: Energy={energy_col}, UserName={username_col}, StartDate={startdate_col}, StartHour={starthour_col}, EndDate={enddate_col}, EndHour={endhour_col}, ChargingTime={chartime_col}")

    rows = []
    for row in reader:
        try:

            UserName = row[username_col].strip()
            StartDate = row[startdate_col].strip()
            StartHour = row[starthour_col].strip()
            EndDate = row[endhour_col].strip()
            EndHour = row[endhour_col].strip()
            ChargingTime = row[chartime_col].strip()
            energy_str = row[energy_col].strip().replace(",", ".")
            energy = float(energy_str)
            
            rows.append((UserName, StartDate, StartHour, EndDate, EndHour, ChargingTime, energy))
        except Exception as e:
            logger.warning(f"Row skipped: {e} - Row data: {row}")
            continue

    if rows:
        cursor.executemany(
            "INSERT INTO GreenWallbox ([UserName], [StartDate], [StartHour], [EndDate], [EndHour], [ChargingTime], [Energy]) VALUES (?, ?, ?, ?, ?, ?, ?)",
            rows
        )
        conn.commit()
        logger.info(f"{len(rows)} records saved to database.")
    else:
        logger.warning("No valid data rows parsed from CSV.")

    conn.close()

# --- Main Logic ---
def main():
    cfg = load_config()
    retry_delay = 900  # 15 minutes

    while True:
        try:
            token = login(cfg)

            now = datetime.now(UTC)
            last_update = datetime.strptime(cfg.get("Update_date", f"{now.year}-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S")
            start_date = (last_update + timedelta(days=1)).strftime("%Y-%m-%d")  # Add one day to last_update
            end_date = now.strftime("%Y-%m-%d")

            zip_data = download_report(cfg, token, start_date, end_date)

            if zip_data:
                save_to_db(cfg, zip_data)
                cfg["Update_date"] = now.strftime("%Y-%m-%d %H:%M:%S")
                save_config(cfg)
                logger.info(f"Config updated with new Update_date: {cfg['Update_date']}")
            else:
                logger.info("No new data found in report.")

            logger.info("Service run completed successfully.")
            break

        except Exception as e:
            logger.error(f"Error occurred: {e}")
            logger.info(f"Retrying in {retry_delay / 60:.0f} minutes...")
            time.sleep(retry_delay)

if __name__ == "__main__":
    main()