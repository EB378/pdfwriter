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
    bold=False,
    underline=False,
    strikethrough=False,
):
    """
    Draws text with options for size, color, background, alignment, and effects (bold, underline, strikethrough).

    Parameters:
        c (canvas): ReportLab canvas object.
        text (str): The text to be drawn.
        x (float): X-coordinate of the text.
        y (float): Y-coordinate of the text.
        size (float): Font size. Default: STANDARD_FONT_SIZE.
        color (Color): Text color. Default: STANDARD_TEXT_COLOR.
        bg_color (Color): Background color of the text. Default: None.
        font (str): Font name. Default: STANDARD_FONT.
        alignment (str): Text alignment ('left', 'center', 'right', 'justify').
        centered (bool): Whether the coordinates refer to the center of the text.
        justify_width (float): Width to justify the text within.
        bold (bool): Whether the text should be bold. Default: False.
        underline (bool): Whether the text should be underlined. Default: False.
        strikethrough (bool): Whether the text should have a strikethrough. Default: False.
    """
    # Use default values if not specified
    font = font or STANDARD_FONT
    if bold and not font.endswith("-Bold"):
        font += "-Bold"
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
    margin = 50  # Adjust as needed
    if x < margin:
        print(f"Warning: Text '{text}' shifted right to fit within left margin.")
        x = margin
    elif x + text_width > PAGE_WIDTH - margin:
        print(f"Warning: Text '{text}' shifted left to fit within right margin.")
        x = PAGE_WIDTH - margin - text_width

    # Draw background color if specified
    if bg_color:
        c.setFillColor(bg_color)
        c.rect(x - 2, y - size, text_width + 4, size + 4, stroke=0, fill=1)

    # Reset text color and draw text
    c.setFillColor(color)
    c.drawString(x, y, text)

    # Draw underline if specified
    if underline:
        c.setLineWidth(1)
        c.setStrokeColor(color)
        c.line(x, y - 2, x + text_width, y - 2)

    # Draw strikethrough if specified
    if strikethrough:
        c.setLineWidth(1)
        c.setStrokeColor(color)
        c.line(x, y + size / 3, x + text_width, y + size / 3)


def draw_image(
    c,
    img_path,
    x,
    y,
    width=None,
    height=None,
    crop=False,
    dim=False,
    dim_amount=50,  # Accepts percentage (0 to 100)
    centered=False,
    crop_top=0,
    crop_bottom=0,
    crop_left=0,
    crop_right=0,
):
    """
    Draws an image with optional cropping, dimming (configurable amount in percentage), and centering.

    Parameters:
        dim_amount (int): Percentage for dimming (0 to 100). Default: 50.
    """
    if not os.path.exists(img_path):
        print(f"Error: Image file '{img_path}' not found.")
        return

    with Image.open(img_path) as img:
        if img.mode == "RGBA":  # Convert RGBA to RGB to support JPEG
            img = img.convert("RGB")

        # Apply cropping if crop=True
        if crop:
            img_width, img_height = img.size
            left = crop_left
            top = crop_top
            right = img_width - crop_right
            bottom = img_height - crop_bottom
            img = img.crop((left, top, right, bottom))

        # Apply dimming if dim=True
        if dim:
            dim_factor = dim_amount / 100  # Convert percentage to a factor (0.0 to 1.0)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(dim_factor)

        # Resize the image if width and height are provided
        if width and height:
            img = img.resize((int(width), int(height)))

        # Generate a unique temporary file for the image
        temp_img_path = f"temp_image_{uuid.uuid4().hex}.jpg"
        img.save(temp_img_path, "JPEG")

        # Adjust X and Y if centered
        if centered and width and height:
            x -= width / 2
            y -= height / 2

        # Draw the image
        c.drawImage(temp_img_path, x, y, width=width, height=height, mask="auto")

        # Remove the temporary file
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
