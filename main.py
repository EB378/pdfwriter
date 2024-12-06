from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from commands import *

PAGE_WIDTH, PAGE_HEIGHT = A4  # A4 Page dimensions
MARGIN = 50
START_Y = PAGE_HEIGHT  # Start Y-coordinate for content
LINE_HEIGHT = 20  # Line spacing for text

def read_input(file_path):
    """Read the input file for PDF instructions."""
    with open(file_path, "r") as f:
        return f.readlines()

def top_down_y(y):
    """Convert a top-down Y-coordinate to the bottom-up system used by ReportLab."""
    return PAGE_HEIGHT - y

def create_pdf(file_name, instructions):
    """
    Generate a multi-page PDF based on the input instructions.
    Each command is processed sequentially, and manual page breaks
    can be added using a special identifier: PAGE_BREAK.
    """
    c = canvas.Canvas(file_name, pagesize=A4)
    y_position = START_Y  # Current Y-coordinate for drawing

    for instruction in instructions:
        parts = instruction.strip().split("||")
        command = parts[0]

        if command == "TEXT":
            text, x, y, size, color, bg_color, font, alignment, centered, justify_width = (
                parts[1],
                int(parts[2]),
                int(parts[3]),
                float(parts[4]) if parts[4] else None,
                parse_color(parts[5]),
                parse_color(parts[6]),
                parts[7] if parts[7] else None,
                parts[8] if parts[8] else None,
                parts[9].lower() == "true" if len(parts) > 9 and parts[9] else False,
                float(parts[10]) if len(parts) > 10 and parts[10] else None,
            )
            draw_text(c, text, x, y, size=size, color=color, bg_color=bg_color, font=font, alignment=alignment, centered=centered, justify_width=justify_width)



        elif command == "UNDERLINE":
            text, x, y, size, color = (
                parts[1],
                int(parts[2]),
                int(parts[3]),
                float(parts[4]) if parts[4] else None,
                colors.HexColor(parts[5]) if parts[5] else None,
            )
            draw_underlined_text(c, text, x, y, size=size, color=color)

        elif command == "STRIKETHROUGH":
            text, x, y, size, color = (
                parts[1],
                int(parts[2]),
                int(parts[3]),
                float(parts[4]) if parts[4] else None,
                colors.HexColor(parts[5]) if parts[5] else None,
            )
            draw_strikethrough_text(c, text, x, y, size=size, color=color)

        elif command == "IMAGE":
            img_path, x, y, width, height, crop, dim, centered = (
                parts[1],
                float(parts[2]),
                float(parts[3]),
                float(parts[4]) if parts[4] else None,
                float(parts[5]) if parts[5] else None,
                parts[6].lower() == "true" if parts[6] else False,
                parts[7].lower() == "true" if parts[7] else False,
                parts[8].lower() == "true" if len(parts) > 8 and parts[8] else False,
            )
            draw_image(c, img_path, x, y, width=width, height=height, crop=crop, dim=dim, centered=centered)


        elif command == "TABLE":
            table_data = eval(parts[1])  # Parse table data as a list of lists
            x, y = int(parts[2]), int(parts[3])
            col_widths = eval(parts[4]) if parts[4] else None
            row_heights = eval(parts[5]) if parts[5] else None
            draw_table(c, table_data, x, y, col_widths=col_widths, row_heights=row_heights)

        elif command == "LINE_BREAK":
            # Reduce Y-coordinate by line height for spacing
            y_position -= LINE_HEIGHT

        elif command == "PAGE_BREAK":
            # Add a page break
            c.showPage()
            y_position = START_Y  # Reset Y-coordinate for the new page

        # Ensure we don't overflow the page
        if y_position < MARGIN and command != "PAGE_BREAK":
            c.showPage()
            y_position = START_Y  # Reset Y-coordinate for the new page

    c.save()

if __name__ == "__main__":
    instructions = read_input("input.txt")
    create_pdf("Generated_PDF.pdf", instructions)
