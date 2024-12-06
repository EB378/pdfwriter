from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from commands import *

def read_input(file_path):
    """Read the input file for PDF instructions."""
    with open(file_path, "r") as f:
        return f.readlines()

def create_pdf(file_name, instructions):
    """Generate a PDF based on the input instructions."""
    c = canvas.Canvas(file_name, pagesize=A4)
    y_position = 800  # Starting Y position for text
    
    for instruction in instructions:
        parts = instruction.strip().split("||")
        command = parts[0]
        
        if command == "TEXT":
            text, x, y, color = parts[1], int(parts[2]), int(parts[3]), parts[4]
            draw_text(c, text, x, y, color=colors.HexColor(color))
        
        elif command == "UNDERLINE":
            text, x, y, color = parts[1], int(parts[2]), int(parts[3]), parts[4]
            draw_underlined_text(c, text, x, y, color=colors.HexColor(color))
        
        elif command == "IMAGE":
            img_path, x, y, width, height = parts[1], int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])
            draw_image(c, img_path, x, y, width=width, height=height)
        
        # Add more commands as needed
        
        y_position -= 20  # Adjust line spacing

    c.save()

if __name__ == "__main__":
    instructions = read_input("input.txt")
    create_pdf("Generated_PDF.pdf", instructions)
