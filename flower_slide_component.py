import os
from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime
from github_upload import upload_to_github

# Configuration
BACKGROUND_PATH = "image_fx (10).jpg"  # Your background image
TITLE_FONT = "arial.ttf"  # Using lowercase for Windows compatibility
BG_TITLE_COLOR = (0, 0, 0, 180)  # Semi-transparent black
BG_CARD_COLOR = (255, 255, 255, 230)  # Semi-transparent white
GITHUB_REPO = "mimjdefender/HourlyFlower"  # GitHub repo in username/repo format

def get_font_path():
    """Get the path to a system font"""
    # Try common Windows font locations
    font_paths = [
        os.path.join(os.environ['WINDIR'], 'Fonts', 'arial.ttf'),
        os.path.join(os.environ['WINDIR'], 'Fonts', 'Arial.ttf'),
        'arial.ttf',
        'Arial.ttf'
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            return path
    
    # If no font found, use default
    return None

def generate_slide_component(store_name, products):
    """
    Generate a slide component for Prismic CMS embedding.
    
    Args:
        store_name (str): Name of the store
        products (list): List of product dictionaries with keys:
            - strain: Product strain name
            - brand: Brand name
            - grams: Weight in grams
            - days_since: Days since harvest
    
    Returns:
        dict: A dictionary containing the slide component data for Prismic CMS
    """
    # Create the image
    if not os.path.exists(BACKGROUND_PATH):
        raise FileNotFoundError(f"Background image not found: {BACKGROUND_PATH}")
    
    img = Image.open(BACKGROUND_PATH).convert("RGBA")
    width = img.size[0]
    
    # Load fonts
    font_path = get_font_path()
    if not font_path:
        raise FileNotFoundError("Could not find a suitable font file")
    
    title_font = ImageFont.truetype(font_path, 48)
    sub_font = ImageFont.truetype(font_path, 38)
    brand_font = ImageFont.truetype(font_path, 34)
    
    # Draw title header
    title = "MOST RECENT HARVEST"
    title_width = title_font.getbbox(title)[2]
    draw_card(img, ((width - title_width) // 2 - 40, 60), [title], [title_font], BG_TITLE_COLOR)
    
    # Draw product cards
    y_start = 170
    for i, product in enumerate(products):
        draw_card(
            img,
            (80, y_start + i * 320),
            [product["strain"], f"Brand: {product['brand']}", product["grams"], product["days_since"]],
            [title_font, brand_font, sub_font, sub_font],
            BG_CARD_COLOR
        )
    
    # Save the image
    output_file = f"flower_slide_{store_name.lower().replace(' ', '_')}.png"
    img.convert("RGB").save(output_file)
    
    # Upload to GitHub and get raw URL
    raw_url = upload_to_github(output_file, GITHUB_REPO)
    if not raw_url:
        raise Exception("Failed to upload image to GitHub")
    
    # Create Prismic CMS embed data
    prismic_data = {
        "type": "embed",
        "data": {
            "url": raw_url,
            "title": f"Flower Harvest - {store_name}",
            "description": f"Latest flower harvest information for {store_name}",
            "thumbnail_url": raw_url,
            "author_name": "Meds Cafe",
            "author_url": "https://medscafe.com",
            "provider_name": "Meds Cafe",
            "provider_url": "https://medscafe.com",
            "cache_age": 3600,  # Cache for 1 hour
            "width": img.size[0],
            "height": img.size[1],
            "html": f'<div class="flower-slide"><img src="{raw_url}" alt="Flower Harvest - {store_name}" /></div>'
        }
    }
    
    # Save the Prismic data
    with open(f"prismic_embed_{store_name.lower().replace(' ', '_')}.json", "w") as f:
        json.dump(prismic_data, f, indent=2)
    
    return prismic_data

def draw_card(img, position, lines, fonts, card_color, font_color="white"):
    """Helper function to draw a card with text"""
    draw_base = ImageDraw.Draw(img)
    padding, radius = 20, 20
    shadow_offset = (6, 6)
    w_max = max(draw_base.textlength(line, font=fonts[i]) for i, line in enumerate(lines))
    h_total = sum(fonts[i].getbbox(line)[3] for i, line in enumerate(lines)) + (len(lines) - 1) * 10
    box_width = int(w_max + 2 * padding)
    box_height = int(h_total + 2 * padding)
    card_img = Image.new("RGBA", (box_width + shadow_offset[0], box_height + shadow_offset[1]), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_img)
    shadow_box = [shadow_offset[0], shadow_offset[1], shadow_offset[0]+box_width, shadow_offset[1]+box_height]
    card_draw.rounded_rectangle(shadow_box, radius, fill=(0,0,0,100))
    card_draw.rounded_rectangle([0,0,box_width,box_height], radius, fill=card_color)
    img.alpha_composite(card_img, position)
    x_text = position[0] + padding
    y_text = position[1] + padding
    for i, line in enumerate(lines):
        draw_base.text((x_text, y_text), line, font=fonts[i], fill=font_color)
        y_text += fonts[i].getbbox(line)[3] + 10

if __name__ == "__main__":
    try:
        # Example usage
        store_name = "Cheboygan"
        products = [
            {
                "strain": "Blue Dream",
                "brand": "Meds Cafe",
                "grams": "3.5g",
                "days_since": "Harvested 5 days ago"
            },
            {
                "strain": "OG Kush",
                "brand": "Meds Cafe",
                "grams": "7g",
                "days_since": "Harvested 3 days ago"
            }
        ]
        
        prismic_data = generate_slide_component(store_name, products)
        print(f"✅ Slide component generated for {store_name}")
        print(f"📄 Prismic embed data saved to prismic_embed_{store_name.lower().replace(' ', '_')}.json")
        print(f"🖼️ Image uploaded to GitHub and saved as flower_slide_{store_name.lower().replace(' ', '_')}.png")
    except Exception as e:
        print(f"❌ Error: {str(e)}") 