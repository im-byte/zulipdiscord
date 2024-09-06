import discord
import yaml
from discord.ext import commands, tasks
from fetcher import ZulipFetcher


latest_msg_ids = []

# Load config
with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Load fetchers
zfs_info = []
zfs = []
for j in range(len(cfg['zrcs'])):
    zfs.append(ZulipFetcher(cfg['zrcs'][j]))
    zfs_info.append(cfg['zrcsinfo'][j])
    latest_msg_ids.append(0)

# Load discord info
token = cfg['discord']['token']
channels = cfg['discord']['channels']

# init bot
prefix = "."
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)


@client.event
async def on_ready():
    print("BOT: Discord Bot online and ready.")
    client.loop.create_task(latest_msg())


@tasks.loop(minutes=1.0, count=None)
async def latest_msg():
    for i in range(len(zfs)):
        zf = zfs[i]
        channel = channels[min(len(channels), i)]
        msgs = zf.fetch_messages(1)

        for msg in msgs:
            if msg[2] != latest_msg_ids[i]:
                embed = discord.Embed(title=msg[0], description=msg[1])
                embed.set_author(name=zfs_info[i])
                await client.get_channel(channel).send(embed=embed)

                latest_msg_ids[i] = msg[2]


client.run(token)
