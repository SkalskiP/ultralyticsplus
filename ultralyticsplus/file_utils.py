from PIL import ImageDraw, ImageFont, ImageEnhance


def add_text_to_image(
    text,
    pil_image,
    brightness: float = 0.75,
    text_font: int = 50,
    crop_margin: int = None,
):

    # Create an ImageEnhance object
    enhancer = ImageEnhance.Brightness(pil_image)

    # Darken the image by 25%
    pil_image = enhancer.enhance(brightness)

    # Resize the image
    pil_image = pil_image.resize((1280, 1280))

    if crop_margin is not None:
        # crop image
        width, height = pil_image.size
        mid_height = int(height / 2)
        min_height = max(0, mid_height - crop_margin)
        max_height = min(height, mid_height + crop_margin)
        pil_image = pil_image.crop((0, min_height, width, max_height))

    # Create an ImageDraw object
    draw = ImageDraw.Draw(pil_image)

    # Define the font and text to be written
    font = ImageFont.truetype("OpenSans-Bold.ttf", text_font)

    # Get the bounding box of the text
    bbox = draw.textbbox((0, 0), text, font=font)

    # Get the width and height of the text
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Define the coordinates of the smaller rounded rectangle
    box_margin = 20
    x1, y1 = (pil_image.width - text_width) / 2 - box_margin, (
        pil_image.height - text_height
    ) / 2 - box_margin / 3
    x2, y2 = (pil_image.width + text_width) / 2 + box_margin, (
        pil_image.height + text_height * 2
    ) / 2 + box_margin / 3

    # Define the radius of the rounded corners
    radius = 15

    # Draw the rounded rectangle
    draw.rounded_rectangle(
        [(x1, y1), (x2, y2)],
        radius=radius,
        fill=(255, 255, 255),
        outline=None,
        width=5,
    )

    # Draw the text on the image
    draw.text(
        ((pil_image.width - text_width) / 2, (pil_image.height - text_height) / 2),
        text,
        font=font,
        fill=(0, 0, 0),
    )

    return pil_image