from sys import path

path.append(r"api")

from discord.ui import View, button, Button
from discord import Interaction, ButtonStyle, Embed, User
from google_sheets_api import (
    get_google_sheets,
    get_google_sheets_values,
    SPREADSHEET_ID,
)
# from sqlite3 import connect

temp = {
    "B": "FM",
    "C": "Stepik",
    "D": "Eolimp",
    "E": "Codeforces",
    "F": "HackerRank",
    "G": "Digər",
}


class MyView1(View):
    def __init__(self, name: str, point: int):
        super().__init__(timeout=None)
        self.name = name
        self.point = point

    @button(label="C++", style=ButtonStyle.primary)
    async def cpp(self, interaction: Interaction, button: Button):
        await self.__response(interaction, "Cpp")

    @button(label="Python", style=ButtonStyle.danger)
    async def python(self, interaction: Interaction, button: Button):
        await self.__response(interaction, "Python")

    async def __response(self, interaction, sheet_name):
        await interaction.response.send_message(
            view=MyView2(self.name, self.point, sheet_name), ephemeral=True
        )


class MyView2(View):
    def __init__(self, name: str, point: int, sheet_name: str):
        super().__init__(timeout=None)
        self.name = name
        self.point = point
        self.sheet_name = sheet_name

    @button(label="FM", style=ButtonStyle.primary)
    async def fm(self, interaction: Interaction, button: Button):
        await self.__foo(interaction, "B")

    @button(label="Stepik", style=ButtonStyle.danger)
    async def stepik(self, interaction: Interaction, button: Button):
        await self.__foo(interaction, "C")

    @button(label="Eolymp", style=ButtonStyle.success)
    async def eolymp(self, interaction: Interaction, button: Button):
        await self.__foo(interaction, "D")

    @button(label="Codeforces", style=ButtonStyle.danger)
    async def codeforces(self, interaction: Interaction, button: Button):
        await self.__foo(interaction, "E")

    @button(label="HackerRank", style=ButtonStyle.primary)
    async def hacker_rank(self, interaction: Interaction, button: Button):
        await self.__foo(interaction, "F")

    @button(label="Digər", style=ButtonStyle.primary)
    async def others(self, interaction: Interaction, button: Button):
        await self.__foo(interaction, "G")

    async def __foo(self, interaction: Interaction, column):
        await interaction.response.send_message(content="done", ephemeral=True)
        if await self.__update_google_sheet_cell(
            self.name, self.sheet_name, column, self.point
        ):
            await interaction.guild.get_channel(1211675591439552532).send(
                embed=MyEmbed(interaction.user, self.name, self.point, temp[column])
            )

    async def __update_google_sheet_cell(
        self, name: str, sheet_name: str, column: str, point: int
    ):
        try:
            sheets = await get_google_sheets()
            values = await get_google_sheets_values(sheets, sheet_name, "A2:G25")

            for i, value in enumerate(values):
                if value[0].startswith(name):
                    break

            sheets.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{sheet_name}!{column}{i+2}",
                valueInputOption="USER_ENTERED",
                body={"values": [[point + int(values[i][ord(column) - 65])]]},
            ).execute()
            return True
        except Exception as e:
            print("Error:", e)
            return False


class MyEmbed(Embed):
    def __init__(self, writer: User, wroten, point, column_name):
        super().__init__(
            colour=0x00A851,
            title="Bal yazıldı",
            description="",
        )
        self.add_field(
            name="Yazan",
            value=f"{writer.mention}",
            inline=False,
        )
        self.add_field(
            name="Yazılan",
            value=f"{wroten}",
            inline=False,
        )
        self.add_field(
            name="Hara",
            value=f"{column_name}",
            inline=False,
        )
        self.add_field(
            name="Bal",
            value=f"{point}",
            inline=False,
        )

        # with connect("database/log.db") as connection:
        #     cursor = connection.cursor()
        #     cursor.execute(
        #         "INSERT INTO Log (writer_discord_id, wroten_name, column_name, point) VALUES (?, ?, ?, ?)",
        #         (writer.id, wroten, column_name, point),
        #     )
        #     cursor.close()
