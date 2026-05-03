import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import traceback
import utils
import paypayu
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN が未設定だから環境変数を確認してね")
if not TOKEN or len(TOKEN) < 50:
    raise ValueError("トークンの形式がおかしい")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    help_command=None
)

async def setup_hook():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cogs_dir = os.path.join(base_dir, "Cogs")

    print(f"[INFO] Cogs dir: {cogs_dir}")

    if not os.path.exists(cogs_dir):
        print("[ERROR] Cogsフォルダが存在しません")
        return

    for file in os.listdir(cogs_dir):
        if file.endswith(".py") and not file.startswith("_"):
            ext = f"Cogs.{file[:-3]}"
            try:
                await bot.load_extension(ext)
                print(f"[OK] Loaded Cog: {ext}")
            except Exception as e:
                print(f"[NG] Failed Cog: {ext}")
                traceback.print_exc()

    await bot.tree.sync()
    print("[INFO] Slash commands synced")

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print("===================================")
    print(f"Bot logged in as {bot.user}")
    print("===================================")

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    print(error)
    traceback.print_exc()
    
if __name__ == "__main__":
    bot.run(TOKEN)
