# PDF Generator with Custom Commands

## Overview
This program generates customizable PDFs using predefined commands specified in the `input.txt` file. The commands allow for text styling, image configurations, and more.

## File Structure
pdf_generator/ ├── main.py # Main script ├── commands.py # Functions for styling ├── input.txt # Editable instructions for the PDF ├── README.md # Documentation

python
Copy code

## Commands
Each command is written in the `input.txt` file with the format:

COMMAND||ARGUMENTS

markdown
Copy code

### Supported Commands
1. **TEXT**:
   - Draws plain text.
   - Format: `TEXT||<text>||<x>||<y>||<color>`
   - Example: `TEXT||Hello World||100||750||#FF0000`

2. **UNDERLINE**:
   - Draws underlined text.
   - Format: `UNDERLINE||<text>||<x>||<y>||<color>`
   - Example: `UNDERLINE||Underlined Text||100||700||#000000`

3. **IMAGE**:
   - Adds an image.
   - Format: `IMAGE||<path>||<x>||<y>||<width>||<height>`
   - Example: `IMAGE||assets/logo.png||50||600||150||75`

## Usage
1. **Edit Input**:
   Update `input.txt` with desired instructions.

2. **Run Script**:
   Generate the PDF:
   ```bash
   python main.py
Output:
The Generated_PDF.pdf file will be created in the same directory.
