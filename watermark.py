from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

def open_image(image_source):
    """Opens an image from a URL or local path."""
    if os.path.exists(image_source):
        # It's a local file path
        return Image.open(image_source)
    else:
        # Assume it's a URL
        response = requests.get(image_source)
        return Image.open(BytesIO(response.content))

def apply_transparent_watermark(original_path, watermark_path, output_path, position=(0, 0)):
    original = Image.open(original_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")
    
    # Create a new image for the output with the same dimensions and RGBA mode
    combined = Image.new("RGBA", original.size)
    
    # Paste the original image into the combined image
    combined.paste(original, (0, 0))
    
    # Paste the watermark into the combined image, using itself as the mask
    combined.paste(watermark, position, watermark)
    
    # If the output needs to be in RGB mode (e.g., for saving as JPEG), convert the mode
    combined = combined.convert("RGB")
    
    combined.save(output_path)

from PIL import Image

def apply_watermark(original_path, watermark_path, output_path, position=(50, 50)):
    original = Image.open(original_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")
    
    # Create a new image for the output with the same dimensions and RGBA mode
    combined = Image.new("RGBA", original.size)
    
    # Paste the original image into the combined image
    combined.paste(original, (0, 0))
    
    # Paste the watermark into the combined image, using itself as the mask
    combined.paste(watermark, position, watermark)
    
    # If the output needs to be in RGB mode (e.g., for saving as JPEG), convert the mode
    combined = combined.convert("RGB")
    
    combined.save(output_path)


# Cleanup function to remove temporary files
def cleanup(*files):
    for file in files:
        os.remove(file)

