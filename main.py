from discord import Intents
from discord.ext.commands import Bot, when_mentioned_or
from os import listdir, getenv
from dotenv import load_dotenv


class Client(Bot):
    def __init__(self):
        super().__init__(command_prefix=when_mentioned_or("/"), intents=Intents.all())

    async def setup_hook(self):
        for filename in listdir("./cogs/commands"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.commands.{filename[:-3]}")

    async def on_ready(self):
        print(f"Bot is ready. Logged in as {self.user.name}")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)


def main():
    load_dotenv()
    TOKEN = getenv("DISCORD_TOKEN")
    client = Client()
    client.run(TOKEN)


if __name__ == "__main__":
    main()
