from sys import path

path.append(r"api")

from discord import Interaction
from discord.ext.commands import Bot, Cog
from discord import app_commands
from views import MyView1
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
        await interaction.response.send_message(
            view=MyView1(interaction.channel.name.capitalize(), point), ephemeral=True
        )

    @app_commands.command(name="reset_db")
    @app_commands.check(is_owner)
    async def reset_db(self, interaction: Interaction):
        reset_db()


async def setup(client):
    await client.add_cog(CommandsCog(client))
