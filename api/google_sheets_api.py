from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from os import getenv, path

current_dir = path.dirname(path.abspath(__file__))

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_KEY_FILE = path.join(current_dir, "service_account_key.json")
SPREADSHEET_ID = getenv("SPREADSHEET_ID")

async def get_google_sheets():
    try:
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY_FILE, scopes=SCOPES
        )
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()
        
        return sheets
    except Exception as e:
        print("Error:", e)
        return None


async def get_google_sheets_values(sheets, sheet_name: str, range: str):
    try:
        temp = f"{sheet_name}!{range}"
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=temp).execute()
        values = result.get("values", [])
        return values
    except Exception as e:
        print("Error:", e)
        return None

