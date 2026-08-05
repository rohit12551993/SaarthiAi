from PIL import Image, ImageDraw
from io import BytesIO
import requests
import os
from datetime import datetime

def load_image(image_path: str):
    # If it's a URL, download it first
    if image_path.startswith('http://') or image_path.startswith('https://'):
        response = requests.get(image_path, timeout=20)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert('RGB')

    # Otherwise treat it as local file
    return Image.open(image_path).convert('RGB')


def annotate_ui_issues(image_path: str, issues: list):
    image = load_image(image_path)

    draw = ImageDraw.Draw(image)

    for idx, issue in enumerate(issues, start=1):
        x1, y1, x2, y2 = issue['bbox']
        label = issue['label']

        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline='red', width=4)

        # Draw label
        draw.text((x1, max(5, y1 - 22)), f'{idx}. {label}', fill='red')

    os.makedirs('annotated_reports', exist_ok=True)

    filename = f"ui_issues_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    output_path = os.path.join('annotated_reports', filename)

    image.save(output_path)

    return output_path
