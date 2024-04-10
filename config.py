import json

def load_channel_settings():
    default_settings = {
        'source_channel': None,
        'destination_channels': [],
        'forwarding_active': False,
        'link_only': False,
        'modify_caption': False,
        'caption_format': '',
        'watermark_enabled': False,
        'watermark_url': ''
    }
    try:
        with open('channel_settings.json', 'r') as file:
            loaded_settings = json.load(file)
            # Update default settings with any loaded values to ensure all keys exist
            default_settings.update(loaded_settings)
            return default_settings
    except (FileNotFoundError, json.JSONDecodeError):
        # Return defaults if file doesn't exist or there's a decoding error
        return default_settings

def save_channel_settings(channel_settings):
    with open('channel_settings.json', 'w') as file:
        json.dump(channel_settings, file, indent=4)  # Added indent for better readability
