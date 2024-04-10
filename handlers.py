from telethon import events
from config import load_channel_settings, save_channel_settings
from watermark import apply_watermark, cleanup
import re
import os
import tempfile
import mimetypes

ALL_EVENTS = {}

async def start(event):
    await event.respond('Hello!')

async def watermark_cmd(event):
    channel_settings = load_channel_settings()

    command_parts = event.message.text.split(maxsplit=1)
    if len(command_parts) == 2:
        action = command_parts[1].lower()

        if action == 'on':
            channel_settings['watermark_enabled'] = True
            response = "Watermark feature enabled."
        elif action == 'off':
            channel_settings['watermark_enabled'] = False
            response = "Watermark feature disabled."
        else:
            response = "Invalid command. Use '/watermark on' to enable or '/watermark off' to disable."
    else:
        response = "Please specify 'on' or 'off'."

    save_channel_settings(channel_settings)
    await event.respond(response)

# Register the watermark command
ALL_EVENTS['watermark_cmd'] = (watermark_cmd, events.NewMessage(pattern="/watermark"))

async def set_source(event, channel_settings):
    try:
        _, channel_id = event.raw_text.split(maxsplit=1)
        channel_settings['source_channel'] = channel_id
        save_channel_settings(channel_settings)
        await event.respond(f"Source channel set to {channel_id}")
    except ValueError:
        await event.respond("Usage: /setsource <channel_id_or_username>")

async def add_destination(event, channel_settings):
    try:
        _, channel_id = event.raw_text.split(maxsplit=1)
        channel_settings['destination_channels'].append(channel_id)
        save_channel_settings(channel_settings)
        await event.respond(f"Added {channel_id} to destination channels")
    except ValueError:
        await event.respond("Usage: /adddest <channel_id_or_username>")

async def clear_destinations(event, channel_settings):
    channel_settings['destination_channels'].clear()
    save_channel_settings(channel_settings)
    await event.respond("Cleared all destination channels.")

async def start_forwarding(event, channel_settings):
    channel_settings['forwarding_active'] = True
    save_channel_settings(channel_settings)
    await event.respond("Message forwarding has been activated.")

async def stop_forwarding(event, channel_settings):
    channel_settings['forwarding_active'] = False
    save_channel_settings(channel_settings)
    await event.respond("Message forwarding has been deactivated.")

async def toggle_link_only_mode(event, channel_settings):
    # Initialize 'link_only' key if it doesn't exist
    if 'link_only' not in channel_settings:
        channel_settings['link_only'] = False
    # Now safely toggle the 'link_only' value
    channel_settings['link_only'] = not channel_settings['link_only']
    save_channel_settings(channel_settings)  # Save updated settings
    mode_status = "enabled" if channel_settings['link_only'] else "disabled"
    await event.respond(f"Link-only mode has been {mode_status}.")

async def modify_caption(event, channel_settings):
    # Split the message to check if the user wants to disable the feature
    parts = event.message.text.split(maxsplit=1)
    
    # If there's only the command or it's followed by "off", disable the modify_caption feature
    if len(parts) == 1 or parts[1].strip().lower() == "off":
        channel_settings['modify_caption'] = False
        await event.respond("Custom caption format has been disabled.")
    else:
        # Otherwise, update the caption format and enable the modify_caption feature
        channel_settings['modify_caption'] = True
        channel_settings['caption_format'] = parts[1]
        await event.respond("Custom caption format set successfully.")
    
    # Save the updated settings
    save_channel_settings(channel_settings)

async def forwarder(event, channel_settings):
    if not channel_settings['source_channel'] or not channel_settings['forwarding_active']:
        return

    if event.chat_id == int(channel_settings['source_channel']):
        media = event.message.media if hasattr(event.message, 'media') else None
        message_content = event.message.message if hasattr(event.message, 'message') else ""
        
        if 'modify_caption' in channel_settings and channel_settings['modify_caption']:
            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            urls = re.findall(url_pattern, message_content)
            message_content = channel_settings['caption_format'].format(link='\n'.join(urls)) if urls else channel_settings['caption_format'].format(link="")

        for dest_channel in channel_settings['destination_channels']:
            try:
                dest_channel_id = int(dest_channel) if isinstance(dest_channel, str) and not dest_channel.startswith('@') else dest_channel
                
                if 'watermark_enabled' in channel_settings and channel_settings['watermark_enabled'] and media:
                    original_media_path = await event.download_media()
                    
                    mime_type, _ = mimetypes.guess_type(original_media_path)
                    extension = mimetypes.guess_extension(mime_type) if mime_type else '.jpg'
                    
                    fd, output_path = tempfile.mkstemp(suffix=extension)
                    os.close(fd)  # Important to close the file descriptor
                    
                    apply_watermark(original_media_path, channel_settings['watermark_url'], output_path)
                    
                    if os.path.exists(output_path):
                        await event.client.send_file(dest_channel_id, output_path, caption=message_content)
                        os.remove(output_path)  # Cleanup after sending
                    else:
                        print("Watermarked file does not exist:", output_path)
                    
                    cleanup(original_media_path)  # Cleanup the original downloaded media
                    
                elif media:
                    await event.client.send_file(dest_channel_id, file=media, caption=message_content, force_document=True)
                else:
                    await event.client.send_message(dest_channel_id, message_content)
            except Exception as e:
                await event.respond(f"Error forwarding message to {dest_channel}: {str(e)}")