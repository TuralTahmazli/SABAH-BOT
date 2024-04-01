from sys import path

path.append(r"api")

from discord import Interaction
from discord.ext.commands import Bot, Cog
from discord import app_commands
from views import MyView1
from google_sheets_api import (
    get_google_sheets,
    get_google_sheets_values,
    SPREADSHEET_ID,
)
from db import reset_db


def is_owner(interaction: Interaction):
    if interaction.user.is_owner():
        return True
    return False


def is_moderator(interaction: Interaction):
    if interaction.user.get_role(1211382535779520632):
        return True
    return False


class CommandsCog(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command(name="write")
    @app_commands.check(is_moderator)
    async def write(self, interaction: Interaction, point: int):
        name = interaction.channel.name.capitalize()
        if name[0] == "I":
            name = name.replace("I", "İ", 1)
        await interaction.response.send_message(
            view=MyView1(name, point), ephemeral=True
        )

    @app_commands.command(name="update_old_rating")
    @app_commands.check(is_moderator)
    async def update_old_rating(self, interaction: Interaction):
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

    @app_commands.command(name="reset_db")
    @app_commands.check(is_owner)
    async def reset_db(self, interaction: Interaction):
        reset_db()


async def setup(client):
    await client.add_cog(CommandsCog(client))
