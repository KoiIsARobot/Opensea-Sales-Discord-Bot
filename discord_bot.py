# ==============Developed by=================
#        ___           ___                 
#       /\__\         /\  \          ___   
#      /:/  /        /::\  \        /\  \  
#     /:/__/        /:/\:\  \       \:\  \ 
#    /::\__\____   /:/  \:\  \      /::\__\
#   /:/\:::::\__\ /:/__/ \:\__\  __/:/\/__/
#   \/_|:|~~|~    \:\  \ /:/  / /\/:/  /   
#      |:|  |      \:\  /:/  /  \::/__/    
#      |:|  |       \:\/:/  /    \:\__\    
#      |:|  |        \::/  /      \/__/    
#       \|__|         \/__/                
# ===========================================

from discord.ext import commands
from discord import Embed, Color

from opensea import OpenseaAPI


OPENSEA_TOKEN = '64ba782904174daea589874706a60d33'

URL = 'https://opensea.io/'
COLLECTION_DISCORD = {}

opensea = OpenseaAPI(apikey=OPENSEA_TOKEN)
bot = commands.Bot('/')


async def discord_post(
    chat_id: int, img_url: str,
    name: str, permalink: str,
    amount: float, currency: str,
    from_user: str, to_user: str,
    exchange_rate: float, seconds
):

    channel = bot.get_channel(chat_id)
    fiat = round(exchange_rate * amount, 2)

    embed = Embed(
        description=f'{name} has just been sold for {amount} {currency} ({fiat}$)\n\n<t:{seconds}:F>',
        colour=Color.from_rgb(249, 222, 75),
        url=permalink,
        title=name
    )
    embed.set_thumbnail(url=img_url)
    embed.add_field(name='From', value=f'[{from_user}]({URL + from_user})')
    embed.add_field(name='To', value=f'[{to_user}]({URL + to_user})')
    embed.set_footer(text='Developed by Koi',icon_url="https://i.ibb.co/2vdQ9Vv/logo-3.png")

    await channel.send(embed=embed)


@bot.command(name='track')
async def track(ctx: commands.Context, collection: str = None):

    data = opensea.assets(collection=collection)


    if not collection:
        return await ctx.send('Pass an argument!')
    if not data.get('assets'):
        return await ctx.send('This collection does not exist!')

    COLLECTION_DISCORD.update({ctx.channel.id: collection})

    await ctx.send(f'Collection: {collection} installed.')
