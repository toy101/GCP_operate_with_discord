import discord
from discord.ext import commands
import os, traceback, subprocess
from time import sleep

bot = commands.Bot(command_prefix='/')

token_path = "token.txt"
try:
    # For local test
    with open(token_path) as f:
        TOKEN = f.read()
        TOKEN = TOKEN.strip()

    SERVICE_ACCOUNT_ID = 'hogehoge @ hogehoge.iam.gserviceaccount.com'
    GCP_PROJECT_NAME = 'hogehoge'
    MINECRAFT_INSTANCE_NAME = 'hogehoge'
    MINECRAFT_INSTANCE_ZONE = 'hogehoge'

except:
    # For deploy on GCP
    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    SERVICE_ACCOUNT_ID = os.environ['SERVICE_ACCOUNT_ID']
    GCP_PROJECT_NAME = os.environ['GCP_PROJECT_NAME']
    MINECRAFT_INSTANCE_NAME = os.environ['MINECRAFT_INSTANCE_NAME']
    MINECRAFT_INSTANCE_ZONE = os.environ['MINECRAFT_INSTANCE_ZONE']


# サーバー起動処理
def server_start():
    command = f'/snap/bin/gcloud --account={SERVICE_ACCOUNT_ID} compute instances start {MINECRAFT_INSTANCE_NAME} --project {GCP_PROJECT_NAME} --zone {MINECRAFT_INSTANCE_ZONE}'
    subprocess.call(command.split())
    return


# サーバー停止処理
def server_stop():
    command = f'/snap/bin/gcloud --account={SERVICE_ACCOUNT_ID} compute instances stop {MINECRAFT_INSTANCE_NAME} --project {GCP_PROJECT_NAME} --zone {MINECRAFT_INSTANCE_ZONE}'
    subprocess.call(command.split())
    return


# Bot起動時に動作する処理
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('-------')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command(aliases=["boot", "start"])
async def boot(ctx):
    await ctx.send("サーバーを起動します")
    server_start()
    sleep(10)
    await ctx.send("サーバーが起動しました！良き冒険を！")


@bot.command(aliases=["shutdown", "stop"])
async def shutdown(ctx):
    await ctx.send("サーバーを停止します")
    server_stop()


bot.run(TOKEN)
