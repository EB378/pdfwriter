from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from commands import *

PAGE_WIDTH, PAGE_HEIGHT = A4  # A4 Page dimensions
MARGIN = 50
START_Y = PAGE_HEIGHT - MARGIN  # Start Y-coordinate for content
LINE_HEIGHT = 20  # Line spacing for text


def read_input(file_path):
    """Read the input file for PDF instructions."""
    with open(file_path, "r") as f:
        return f.readlines()


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
            text, x, color = parts[1], int(parts[2]), parts[3]
            draw_text(c, text, int(x), int(y_position), color=colors.HexColor(color))
            y_position -= LINE_HEIGHT

        elif command == "UNDERLINE":
            text, x, color = parts[1], int(parts[2]), parts[3]
            draw_underlined_text(c, text, int(x), int(y_position), color=colors.HexColor(color))
            y_position -= LINE_HEIGHT

        elif command == "IMAGE":
            img_path, x, y, width, height = parts[1], int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])
            draw_image(c, img_path, x, y_position - height, width=width, height=height)
            y_position -= height + LINE_HEIGHT

        elif command == "PAGE_BREAK":
            # Add a page break
            c.showPage()
            y_position = START_Y  # Reset Y-coordinate for the new page

        elif command == "LINE_BREAK":
            # Add a line break by reducing the Y-coordinate
            y_position -= LINE_HEIGHT

        # Add more commands here as needed...

        # Ensure we don't overflow the page
        if y_position < MARGIN and command != "PAGE_BREAK":
            c.showPage()
            y_position = START_Y  # Reset Y-coordinate for the new page

    c.save()


if __name__ == "__main__":
    instructions = read_input("input.txt")
    create_pdf("Generated_PDF.pdf", instructions)
