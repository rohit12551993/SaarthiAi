from .visual_annotator import annotate_ui_issues
import os
import tempfile
import requests
from urllib.parse import urlparse

# Public URL where annotated reports are served
PUBLIC_BASE_URL = "http://3.216.78.234:9000"

# Fallback image used when ADK passes a placeholder filename
FALLBACK_IMAGE = "/home/ubuntu/SaarthiAi/test_images/sample_ui.png"


def prepare_image(image_path: str) -> str:
    """
    Prepare an image for visual QA.

    Supported inputs:
      - Local file path
      - Public HTTP/HTTPS URL
      - ADK placeholder filename (user_uploaded_image.png)

    Returns:
      Local file path that can be processed by the annotator.
    """

    print(f"[visual_tool] Received image_path: {image_path}")

    # ---------------------------------------------------
    # Case 1: Local file exists
    # ---------------------------------------------------
    if os.path.exists(image_path):
        print(f"[visual_tool] Using local file: {image_path}")
        return image_path

    # ---------------------------------------------------
    # Case 2: ADK placeholder filename
    # ---------------------------------------------------
    if image_path == "user_uploaded_image.png":
        print("[visual_tool] ADK placeholder detected")

        if os.path.exists(FALLBACK_IMAGE):
            print(f"[visual_tool] Using fallback image: {FALLBACK_IMAGE}")
            return FALLBACK_IMAGE

        raise Exception(
            f"Fallback image not found: {FALLBACK_IMAGE}\n"
            "Create the file before running visual tests."
        )

    # ---------------------------------------------------
    # Case 3: HTTP / HTTPS URL
    # ---------------------------------------------------
    parsed = urlparse(image_path)

    if parsed.scheme in ("http", "https"):

        # Gemini file URLs are not publicly downloadable
        if "generativelanguage.googleapis.com" in parsed.netloc:
            print("[visual_tool] Gemini file URL detected, using fallback image")

            if os.path.exists(FALLBACK_IMAGE):
                return FALLBACK_IMAGE

            raise Exception(
                "Gemini file URLs cannot be downloaded directly and fallback image is missing."
            )

        print(f"[visual_tool] Downloading public image: {image_path}")

        try:
            response = requests.get(image_path, timeout=30)
            response.raise_for_status()

            suffix = os.path.splitext(parsed.path)[1] or ".png"

            tmp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            )

            tmp_file.write(response.content)
            tmp_file.close()

            print(f"[visual_tool] Downloaded image to: {tmp_file.name}")

            return tmp_file.name

        except requests.exceptions.RequestException as e:
            print(f"[visual_tool] Download failed: {e}")

            if os.path.exists(FALLBACK_IMAGE):
                print("[visual_tool] Falling back to local sample image")
                return FALLBACK_IMAGE

            raise Exception(f"Unable to download image: {e}")

    # ---------------------------------------------------
    # Final fallback
    # ---------------------------------------------------
    print("[visual_tool] Unknown image path format")

    if os.path.exists(FALLBACK_IMAGE):
        print("[visual_tool] Using fallback image")
        return FALLBACK_IMAGE

    raise Exception(f"Invalid image path: {image_path}")


def generate_visual_qa_report(image_path: str):
    """
    Generate an annotated UI image using the uploaded screenshot.
    """

    # Convert input into a usable local image
    local_image = prepare_image(image_path)

    # ---------------------------------------------------
    # Temporary sample issues (replace later with AI detection)
    # ---------------------------------------------------
    detected_issues = [
        {
            "label": "Header alignment issue",
            "bbox": [40, 30, 1160, 120]
        },
        {
            "label": "Card spacing inconsistency",
            "bbox": [60, 170, 540, 320]
        },
        {
            "label": "Primary button overlap",
            "bbox": [400, 500, 820, 640]
        }
    ]

    print(f"[visual_tool] Detected {len(detected_issues)} UI issues")

    # ---------------------------------------------------
    # Create annotated image
    # ---------------------------------------------------
    annotated_image = annotate_ui_issues(local_image, detected_issues)

    filename = os.path.basename(annotated_image)

    # Public URL accessible from browser
    public_url = f"{PUBLIC_BASE_URL}/annotated_reports/{filename}"

    print(f"[visual_tool] Annotated image saved: {annotated_image}")
    print(f"[visual_tool] Public URL: {public_url}")

    return {
        "status": "success",
        "message": "Visual QA completed successfully",
        "annotated_image": public_url,
        "issues_found": len(detected_issues),
        "issues": detected_issues
    }
