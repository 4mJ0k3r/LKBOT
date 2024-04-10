from telethon import TelegramClient, events
from handlers import *
from config import load_channel_settings
from handlers import watermark_cmd 

api_id = 'Your_API_KEY'
api_hash = 'Your_API_Hash'
bot_token = 'Bot_Token'

client = TelegramClient('forwarder_bot', api_id, api_hash).start(bot_token=bot_token)

# Load channel settings
channel_settings = load_channel_settings()

# Register handlers
client.on(events.NewMessage(pattern='/start'))(start)
client.on(events.NewMessage(pattern="/watermark"))(watermark_cmd)
client.on(events.NewMessage(pattern='/setsource'))(lambda e: set_source(e, channel_settings))
client.on(events.NewMessage(pattern='/adddest'))(lambda e: add_destination(e, channel_settings))
client.on(events.NewMessage(pattern='/cleardest'))(lambda e: clear_destinations(e, channel_settings))
client.on(events.NewMessage(pattern='/linkonly'))(lambda e: toggle_link_only_mode(e, channel_settings))
client.on(events.NewMessage(pattern='/startforwarding'))(lambda e: start_forwarding(e, channel_settings))
client.on(events.NewMessage(pattern='/modifycaption'))(lambda e: modify_caption(e, channel_settings))
client.on(events.NewMessage(pattern='/stopforwarding'))(lambda e: stop_forwarding(e, channel_settings))
client.on(events.NewMessage)(lambda e: forwarder(e, channel_settings))

def main():
    print("Bot is running...")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
