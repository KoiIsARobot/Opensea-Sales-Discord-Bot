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

import datetime
import asyncio

from opensea import OpenseaAPI, utils

from discord_bot import bot, discord_post, COLLECTION_DISCORD


DISCORD_TOKEN = '...'
OPENSEA_TOKEN = '...'

opensea = OpenseaAPI(apikey=OPENSEA_TOKEN)


async def task():

    while True:

        for chat_id, collection in COLLECTION_DISCORD.items():
            now = datetime.datetime.now()

            data = opensea.events(
                occurred_after=now - datetime.timedelta(seconds=110),
                collection_slug=collection,
                event_type='successful',
                occurred_before=now,
                limit=5
            )
            events = data.get('asset_events')

            for event in events:
                buyer = event.get('winner_account')
                amount = event.get('total_price')
                seller = event.get('seller')

                from_user = seller.get('user') and seller.get('user').get('username')
                to_user = buyer.get('user') and buyer.get('user').get('username')

                date_time = utils.str_to_datetime_utc(event.get('created_date'))

                await discord_post(
                    chat_id=chat_id,
                    img_url=event.get('asset').get('image_url'),
                    name=event.get('asset').get('name'),
                    permalink=event.get('asset').get('permalink'),
                    amount=int(amount[::-1][15:][::-1]) / 1000,
                    currency=event.get('payment_token').get('symbol'),
                    from_user=from_user or seller.get('address'),
                    to_user=to_user or buyer.get('address'),
                    exchange_rate=float(event.get('payment_token').get('usd_price')),
                    seconds=int(date_time.timestamp())
                )

        await asyncio.sleep(110)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    loop.create_task(task())

    bot.loop = loop
    bot.run(DISCORD_TOKEN)
