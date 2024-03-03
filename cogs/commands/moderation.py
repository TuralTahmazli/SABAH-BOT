from sys import path

path.append(r"api")

from discord import Interaction
from discord.ext.commands import Bot, Cog
from discord import app_commands
from views import MyView1

def is_admin(interaction: Interaction):
    if interaction.user.get_role(1211382535779520632):
        return True
    return False


class CommandsCog(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command(name="write")
    @app_commands.check(is_admin)
    async def write(self, interaction: Interaction, point: int):
        await interaction.response.send_message(
            view=MyView1(interaction.channel.name.capitalize(), point), ephemeral=True
        )

async def setup(client):
    await client.add_cog(CommandsCog(client))
