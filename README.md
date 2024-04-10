# Custom Telegram Forwarder Bot with Watermarking Feature

This bot is a versatile Telegram automation tool designed for content creators, businesses, or channel administrators. It automates message forwarding from a source channel to multiple destination channels, with advanced features like watermarking, caption modification, and URL extraction.

## Key Features

- **Automated Message Forwarding**: Seamlessly forwards messages from a specified source channel to one or more destination channels.
- **Dynamic Watermarking**: Automatically applies a customizable watermark to media files (images, videos, GIFs) before forwarding, helping to protect and brand your content.
- **Caption Modification**: Offers the ability to dynamically modify message captions, perfect for inserting call-to-actions or other important links.
- **URL Extraction**: Detects URLs within messages, allowing for potential modifications or analytics tracking.
- **Configurable Settings**: Flexible settings for specifying source and destination channels, watermark details, and other operational parameters.
- **Privacy-Focused**: Does not store media longer than necessary, ensuring forwarded content is handled securely and efficiently.

## Usage Scenarios

- **Content Syndication**: Ideal for creators wanting to distribute their content across multiple channels without manual reposting.
- **Brand Promotion**: Businesses can ensure consistent brand presence across Telegram channels by using watermarked content.
- **Information Dissemination**: Perfect for news outlets or informational channels that aim to spread information quickly to diverse audience segments.

## Getting Started

1. **Configure the Bot**: Set up your bot's source channel, destination channels, and watermark settings according to your needs.
2. **Deploy the Bot**: Run your bot on your preferred server or hosting service.
3. **Monitor and Adjust**: Keep an eye on your bot's activity. Adjust configurations as needed to optimize performance.

## Configuration

Adjust the bot's settings by editing the `channel_settings.json` file or through specific commands to dynamically change its behavior.

Example `channel_settings.json`:

```json
{
  "source_channel": "-100xxxxxxxxxx",
  "destination_channels": ["-100xxxxxxxxxx", "@channelusername"],
  "forwarding_active": true,
  "link_only": false,
  "modify_caption": true,
  "caption_format": "This is my caption \\n{link}\\n\\nAnother caption",
  "watermark_enabled": true,
  "watermark_url": "https://example.com/path/to/watermark.png"
}
