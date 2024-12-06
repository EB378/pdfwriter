from reportlab.lib import colors
from reportlab.pdfgen import canvas
from PIL import Image, ImageEnhance

def set_font(c, font="Helvetica", size=12):
    """Set the font and size for the canvas."""
    c.setFont(font, size)

def draw_text(c, text, x, y, color=colors.black):
    """Draw text with a specified color."""
    c.setFillColor(color)
    c.drawString(x, y, text)

def draw_underlined_text(c, text, x, y, color=colors.black, font="Helvetica", size=12):
    """Draw text with an underline."""
    set_font(c, font, size)
    text_width = c.stringWidth(text, font, size)
    draw_text(c, text, x, y, color)
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.line(x, y - 2, x + text_width, y - 2)

def draw_bold_text(c, text, x, y, color=colors.black):
    """Draw bold text."""
    draw_text(c, text, x, y, color=color, font="Helvetica-Bold", size=12)

def draw_strikethrough_text(c, text, x, y, color=colors.black, font="Helvetica", size=12):
    """Draw text with a strikethrough."""
    set_font(c, font, size)
    text_width = c.stringWidth(text, font, size)
    draw_text(c, text, x, y, color)
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.line(x, y + size / 3, x + text_width, y + size / 3)

def draw_dimmed_text(c, text, x, y, dimming_factor=0.5, font="Helvetica", size=12):
    """Draw dimmed text."""
    color = colors.Color(0, 0, 0, alpha=dimming_factor)
    draw_text(c, text, x, y, color=color, font=font, size=size)

def draw_image(c, img_path, x, y, width=None, height=None, crop=False, dim=False):
    """Draw an image with optional cropping and dimming."""
    with Image.open(img_path) as img:
        if crop:
            img = img.crop((10, 10, img.width - 10, img.height - 10))
        if dim:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.5)
        if width and height:
            img = img.resize((width, height))
        temp_img_path = "temp_image.jpg"
        img.save(temp_img_path)
        c.drawImage(temp_img_path, x, y, width=width, height=height, mask="auto")

def parse_text_effects(c, text, x, y, effects):
    """Apply multiple effects to text."""
    if "underline" in effects:
        draw_underlined_text(c, text, x, y, color=effects.get("color", colors.black))
    elif "bold" in effects:
        draw_bold_text(c, text, x, y, color=effects.get("color", colors.black))
    elif "strikethrough" in effects:
        draw_strikethrough_text(c, text, x, y, color=effects.get("color", colors.black))
    elif "dim" in effects:
        draw_dimmed_text(c, text, x, y, dimming_factor=effects.get("dimming_factor", 0.5))
    else:
        draw_text(c, text, x, y, color=effects.get("color", colors.black))
