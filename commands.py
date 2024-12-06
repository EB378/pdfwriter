from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import uuid
from PIL import Image, ImageEnhance


# Default configurations
STANDARD_FONT = "Helvetica"
STANDARD_FONT_SIZE = 12
STANDARD_TEXT_COLOR = colors.black
PAGE_WIDTH, PAGE_HEIGHT = A4  # A4 Page dimensions
MARGIN = 50
START_Y = PAGE_HEIGHT  # Start Y-coordinate for content
LINE_HEIGHT = 20  # Line spacing for text

def parse_color(color_string):
    """
    Parses a color string into a ReportLab color object.
    If the string is 'none' or empty, returns None.
    """
    if not color_string or color_string.lower() == "none":
        return None
    return colors.HexColor(color_string)


def draw_text(
    c,
    text,
    x,
    y,
    size=None,
    color=None,
    bg_color=None,
    font=None,
    alignment=None,
    centered=False,
    justify_width=None,
):
    """
    Draws text with optional size, color, background color, alignment, and centering,
    while ensuring it stays within the page boundaries.

    Parameters:
        c (canvas): ReportLab canvas object.
        text (str): The text to be drawn.
        x (float): X-coordinate of the text.
        y (float): Y-coordinate of the text.
        size (float): Font size. Default: STANDARD_FONT_SIZE.
        color (Color): Text color. Default: STANDARD_TEXT_COLOR.
        bg_color (Color): Background color of the text. Default: None.
        font (str): Font name. Default: STANDARD_FONT.
        alignment (str): Text alignment ('left', 'center', 'right', 'justify'). Default: None.
        centered (bool): Whether the coordinates refer to the center of the text.
        justify_width (float): Width to justify the text within. Required for 'justify' alignment.
    """
    # Use default values if not specified
    font = font or STANDARD_FONT
    size = size or STANDARD_FONT_SIZE
    color = color or STANDARD_TEXT_COLOR

    c.setFont(font, size)
    c.setFillColor(color)

    # Calculate text width
    text_width = c.stringWidth(text, font, size)

    # Adjust coordinates for centering
    if centered:
        x -= text_width / 2
        y -= size / 2

    # Ensure text stays within page boundaries
    if x < MARGIN:
        print(f"Warning: Text '{text}' shifted right to fit within left margin.")
        x = MARGIN
    elif x + text_width > PAGE_WIDTH - MARGIN:
        print(f"Warning: Text '{text}' shifted left to fit within right margin.")
        x = PAGE_WIDTH - MARGIN - text_width

    if y < MARGIN + size:
        print(f"Warning: Text '{text}' shifted up to fit within bottom margin.")
        y = MARGIN + size
    elif y > PAGE_HEIGHT - MARGIN:
        print(f"Warning: Text '{text}' shifted down to fit within top margin.")
        y = PAGE_HEIGHT - MARGIN

    # Handle text alignment
    if alignment == "center":
        x -= text_width / 2
    elif alignment == "right":
        x -= text_width
    elif alignment == "justify" and justify_width:
        words = text.split()
        space_width = (justify_width - sum(c.stringWidth(w, font, size) for w in words)) / (len(words) - 1)
        cursor_x = x
        for word in words:
            c.drawString(cursor_x, y, word)
            cursor_x += c.stringWidth(word, font, size) + space_width
        return  # Exit the function after justification

    # Draw background color if specified
    if bg_color:
        c.setFillColor(bg_color)
        c.rect(x - 2, y - size, text_width + 4, size + 4, stroke=0, fill=1)

    # Reset text color and draw text
    c.setFillColor(color)
    c.drawString(x, y, text)


def draw_underlined_text(c, text, x, y, size=None, color=None):
    """
    Draws underlined text.

    Parameters:
        c (canvas): ReportLab canvas object.
        text (str): Text to underline.
        x (float): X-coordinate.
        y (float): Y-coordinate.
        size (float): Font size.
        color (Color): Text color.
    """
    draw_text(c, text, x, y, size=size, color=color)
    text_width = c.stringWidth(text, STANDARD_FONT, size or STANDARD_FONT_SIZE)
    c.setStrokeColor(color or STANDARD_TEXT_COLOR)
    c.setLineWidth(1)
    c.line(x, y - 2, x + text_width, y - 2)


def draw_strikethrough_text(c, text, x, y, size=None, color=None):
    """
    Draws strikethrough text.

    Parameters:
        c (canvas): ReportLab canvas object.
        text (str): Text to strikethrough.
        x (float): X-coordinate.
        y (float): Y-coordinate.
        size (float): Font size.
        color (Color): Text color.
    """
    draw_text(c, text, x, y, size=size, color=color)
    text_width = c.stringWidth(text, STANDARD_FONT, size or STANDARD_FONT_SIZE)
    c.setStrokeColor(color or STANDARD_TEXT_COLOR)
    c.setLineWidth(1)
    c.line(x, y + (size or STANDARD_FONT_SIZE) / 3, x + text_width, y + (size or STANDARD_FONT_SIZE) / 3)


def draw_image(c, img_path, x, y, width=None, height=None, crop=False, dim=False, centered=False):
    """
    Draws an image with optional cropping, dimming, and centering.

    Parameters:
        c (canvas): ReportLab canvas object.
        img_path (str): Path to the image.
        x (float): X-coordinate of the image's center (if `centered` is True).
        y (float): Y-coordinate of the image's center (if `centered` is True).
        width (float): Width of the image.
        height (float): Height of the image.
        crop (bool): Whether to crop the image. Default: False.
        dim (bool): Whether to dim the image. Default: False.
        centered (bool): Whether the coordinates refer to the center of the image.
    """
    if not os.path.exists(img_path):
        print(f"Error: Image file '{img_path}' not found.")
        return

    with Image.open(img_path) as img:
        if img.mode == "RGBA":  # Convert RGBA to RGB to support JPEG
            img = img.convert("RGB")

        if crop:
            img = img.crop((10, 10, img.width - 10, img.height - 10))
        if dim:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.5)
        if width and height:
            img = img.resize((int(width), int(height)))

        # Use a unique name for the temporary file
        temp_img_path = f"temp_image_{uuid.uuid4().hex}.jpg"
        img.save(temp_img_path, "JPEG")

        # Adjust X and Y if centered
        if centered and width and height:
            x -= width / 2
            y -= height / 2

        c.drawImage(temp_img_path, x, y, width=width, height=height, mask="auto")
        os.remove(temp_img_path)


def draw_table(c, data, x, y, col_widths=None, row_heights=None, styles=None):
    """
    Draws a table with custom data and styles.

    Parameters:
        c (canvas): ReportLab canvas object.
        data (list): 2D list representing table rows and cells.
        x (float): X-coordinate of the table.
        y (float): Y-coordinate of the table.
        col_widths (list): List of column widths.
        row_heights (list): List of row heights.
        styles (TableStyle): Custom table styles.
    """

    # Ensure row_heights matches the number of rows in data
    num_rows = len(data)
    if row_heights and len(row_heights) != num_rows:
        print(f"Warning: Adjusting row heights to match {num_rows} rows.")
        row_heights = row_heights[:num_rows] + [None] * (num_rows - len(row_heights))

    table = Table(data, colWidths=col_widths, rowHeights=row_heights)
    default_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FF6600")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ])
    table.setStyle(styles or default_style)
    table.wrapOn(c, x, y)
    table.drawOn(c, x, y - table._height)
