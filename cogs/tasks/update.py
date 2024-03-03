from sys import path

path.append(r"api")

from discord.ext.commands import Bot, Cog
from discord.ext import tasks
from discord import app_commands
from google_sheets_api import (
    get_google_sheets,
    get_google_sheets_values,
    SPREADSHEET_ID,
)
from pytz import timezone
from datetime import datetime

azt_timezone = timezone("Asia/Baku")


class UpdateCog(Cog):
    def __init__(self, client: Bot):
        self.client = client
        self.update_old_rating.start()

    def is_friday():
        now = datetime.now(azt_timezone)
        if now.weekday() == 4 and 13 <= now.hour <= 18:
            return True
        return False

    @tasks.loop(hours=1)
    @app_commands.check(is_friday)
    async def update_old_rating(self):
        await self.__update_old_rating()

    @update_old_rating.before_loop
    async def before_update_old_rating(self):
        await self.wait_until_ready()

    async def __update_old_rating(self):
        try:
            sheet_names = ["Cpp", "Python", "Ümumi"]
            range1, range2 = "H2:H25", "I2:I25"

            sheets = await get_google_sheets()

            for sheet_name in sheet_names:
                values = await get_google_sheets_values(sheets, sheet_name, range1)
                sheets.values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"{sheet_name}!{range2}",
                    valueInputOption="USER_ENTERED",
                    body={"values": values},
                ).execute()
            return True
        except Exception as e:
            print("Error:", e)
            return False


async def setup(client):
    await client.add_cog(UpdateCog(client))
