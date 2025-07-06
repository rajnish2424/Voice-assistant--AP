import os
import json
import gspread
from google.oauth2.service_account import Credentials

def get_sheet():
    #Step 1: Load the credentials from environment variable
    raw_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if not raw_json:
        raise ValueError("❌ GOOGLE_CREDENTIALS_JSON not found in environment variables.")

    try:
        #Step 2: Parse the escaped JSON string
        parsed_credentials = json.loads(raw_json)

        #Step 3: Authenticate using the parsed credentials
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(parsed_credentials, scopes=scopes)

        #Step 4: Connect to Google Sheets
        client = gspread.authorize(creds)

        #Step 5: Open the sheet by ID
        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        if not sheet_id:
            raise ValueError("❌ GOOGLE_SHEET_ID not found in environment variables.")

        spreadsheet = client.open_by_key(sheet_id)
        worksheet = spreadsheet.sheet1  # or use .worksheet('Sheet1') if you named it
        return worksheet

    except Exception as e:
        raise RuntimeError(f"❌ Failed to connect to Google Sheets: {str(e)}")
