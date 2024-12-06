Here’s the updated **`README.md`** file with the new functionality for configuring **dimming amount (0-100)**, integrated bold/underline/strikethrough options in the `TEXT` command, and cropping parameters for images.

---

# **PDF Generator with Dynamic Commands**

## **Overview**

This project is a dynamic PDF generator that allows users to create customized PDFs by specifying commands in an `input.txt` file. The system supports text, images, tables, and more, with advanced options such as alignment, dimming, effects (bold, underline, strikethrough), and boundary enforcement.

---

## **Project Structure**

```
pdf_generator/
├── main.py                # Main script for processing commands and generating the PDF
├── commands.py            # Functions for drawing elements on the PDF
├── input.txt              # Command file with instructions for the PDF
├── watcher.py             # Automatically re-runs main.py on input.txt changes
├── README.md              # Documentation for the project
└── assets/                # Directory for storing images (e.g., logos, backgrounds)
    ├── logo.png
    ├── header_bg.jpg
    └── checklist_bg.jpg
```

---

## **Key Features**

1. **Dynamic Commands**: Customize text, images, tables, and other elements in your PDF.
2. **Enhanced Text Options**: 
   - Font size, colors, background colors.
   - Alignment: `left`, `right`, `center`, or `justify`.
   - Effects: Bold, underline, and strikethrough.
3. **Image Features**:
   - Configurable dimming amount (0-100%).
   - Cropping with fine-grained offsets for each side.
   - Centered placement.
4. **Table Creation**: Generate tables with custom data, column widths, and styles.
5. **Multi-Page Support**: Add page breaks and manage content across multiple pages.
6. **Automatic Watcher**: Use `watcher.py` to auto-generate the PDF on changes to `input.txt`.

---

## **Commands Reference**

### **1. `TEXT`**
Adds a line of text with various customization options, including effects.

- **Format**:
  ```
  TEXT||<text>||<x>||<y>||<size>||<color>||<bg_color>||<font>||<alignment>||<centered>||<justify_width>||<bold>||<underline>||<strikethrough>
  ```
- **Parameters**:
  - `<text>`: The text to be added.
  - `<x>`: X-coordinate for the text (center if `centered=true`).
  - `<y>`: Y-coordinate for the text (center if `centered=true`).
  - `<size>`: Font size (e.g., `12` or `16`). Leave blank for default.
  - `<color>`: Hexadecimal color for the text (e.g., `#FF6600`). Leave blank for default.
  - `<bg_color>`: Hexadecimal background color of the text. Leave blank for none.
  - `<font>`: Font name (e.g., `Helvetica-Bold`). Leave blank for default.
  - `<alignment>`: Text alignment (`left`, `center`, `right`, `justify`). Leave blank for default.
  - `<centered>`: `true` to use coordinates as the center of the text. Default: `false`.
  - `<justify_width>`: Width to justify the text within. Required for `justify` alignment.
  - `<bold>`: `true` for bold text.
  - `<underline>`: `true` for underlined text.
  - `<strikethrough>`: `true` for strikethrough text.
- **Example**:
  ```
  TEXT||Bold and Underlined Text||150||500||14||#FF6600||none||Helvetica||center||true||||true||true||false
  TEXT||Justified Text Example||50||750||12||#333333||none||Helvetica||||true||400||false||false||false
  ```

---

### **2. `IMAGE`**
Adds an image with optional resizing, dimming, and cropping.

- **Format**:
  ```
  IMAGE||<path>||<x>||<y>||<width>||<height>||<crop>||<dim>||<dim_amount>||<centered>||<crop_top>||<crop_bottom>||<crop_left>||<crop_right>
  ```
- **Parameters**:
  - `<path>`: Path to the image file (e.g., `assets/logo.png`).
  - `<x>`: X-coordinate of the image’s center (if `centered=true`).
  - `<y>`: Y-coordinate of the image’s center (if `centered=true`).
  - `<width>`: Width of the image.
  - `<height>`: Height of the image.
  - `<crop>`: `true` to crop the image; `false` otherwise.
  - `<dim>`: `true` to dim the image; `false` otherwise.
  - `<dim_amount>`: Percentage of brightness (0 to 100). Defaults to `50`.
  - `<centered>`: `true` to use coordinates as the center of the image. Default: `false`.
  - `<crop_top>`: Pixels to crop from the top. Default: `0`.
  - `<crop_bottom>`: Pixels to crop from the bottom. Default: `0`.
  - `<crop_left>`: Pixels to crop from the left. Default: `0`.
  - `<crop_right>`: Pixels to crop from the right. Default: `0`.
- **Example**:
  ```
  IMAGE||assets/logo.png||300||300||200||100||true||true||70||true||10||20||5||5
  ```

---

### **3. `TABLE`**
Creates a table with rows and columns.

- **Format**:
  ```
  TABLE||<data>||<x>||<y>||<col_widths>||<row_heights>
  ```
- **Parameters**:
  - `<data>`: 2D list for table rows and columns (e.g., `[['Header1', 'Header2'], ['Row1-Col1', 'Row1-Col2']]`).
  - `<x>`: X-coordinate for the table.
  - `<y>`: Y-coordinate for the table.
  - `<col_widths>`: List of column widths. Leave blank for auto-width.
  - `<row_heights>`: List of row heights. Leave blank for auto-height.
- **Example**:
  ```
  TABLE||[['Task', 'Due Date', 'Complete'], ['Pack', '12/10/2023', '[ ]'], ['Move', '12/15/2023', '[ ]']]||50||700||[150, 100, 80]||None
  ```

---

### **4. `LINE_BREAK`**
Adds vertical spacing between lines.

- **Format**:
  ```
  LINE_BREAK
  ```

---

### **5. `PAGE_BREAK`**
Inserts a new page in the PDF.

- **Format**:
  ```
  PAGE_BREAK
  ```

---

## **Usage**

1. **Edit `input.txt`**:
   - Add commands to customize your PDF (refer to the commands above).

2. **Run `main.py`**:
   - Generate the PDF:
     ```bash
     python main.py
     ```

3. **Output**:
   - The generated PDF will be saved as `Generated_PDF.pdf` in the project directory.

---

## **Using `watcher.py`**

For auto-generating the PDF on changes to `input.txt`:
1. Run `watcher.py`:
   ```bash
   python watcher.py
   ```
2. Modify and save `input.txt`.
3. The PDF will be updated automatically.

---

## **Future Enhancements**
- Support for multi-column layouts.
- Interactive forms with checkboxes.
- Auto-generation of headers and footers.

---

Let me know if you need further updates or have additional requirements! 🚀