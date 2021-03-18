from PIL import Image, ImageDraw, ImageFont
import textwrap

# Creates an image and saves it at a specified image path
def create_image(current_question, image_path):

    # Swiss 911 Compressed
    swiss = ImageFont.truetype("fonts/Swiss 911 Compressed.ttf", 120)
    korinna = ImageFont.truetype("fonts/ITC Korinna Regular.ttf", 100)

    # Background
    img = Image.new("RGB", (1600, 900), color=(4, 11, 121))
    d = ImageDraw.Draw(img)

    # Category
    category_lines = textwrap.wrap(current_question["category"], width=20)
    category_formatted = category_lines[0] + "" if len(category_lines) == 1 else "..."
    shadow_text(d, 50, 20, category_formatted.upper(), swiss, 255, 255, 255)

    # Value
    value_formatted = (
        "No Value"
        if current_question["value"] == "None"
        else "$" + current_question["value"]
    )
    w = d.textsize(value_formatted, font=swiss)
    shadow_text(d, 1550 - w[0], 20, value_formatted, swiss, 206, 174, 94)

    # Question
    question_lines = textwrap.wrap(current_question["question"], width=30)
    y = 260
    for line in question_lines:
        w = d.textsize(line, font=korinna)
        shadow_text(d, 800 - w[0] / 2, y, line, korinna, 255, 255, 255)
        y += 120
    img.save(image_path)


# Normal text, but duplicated and translated underneath to create a shadow effect
def shadow_text(d, x, y, text, font, r, g, b):
    d.text((x + 5, y + 5), text, font=font, fill=(0, 0, 0))
    d.text((x, y), text, font=font, fill=(r, g, b))
