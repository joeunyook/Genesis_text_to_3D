import os
import subprocess
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai

# Initialize Vertex AI
vertexai.init(project="tmi-reddit-content-moderation", location="us-central1")

# 🧠 Compute project root (2 levels up from this file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 🔗 Absolute paths based on project root
TRIPOSR_DIR = os.path.join(PROJECT_ROOT, "TripoSR")
IMAGE_PATH = os.path.join(TRIPOSR_DIR, "examples", "generated.png")
OUTPUT_DIR = os.path.join(TRIPOSR_DIR, "output")
TRIPOSR_RUN = os.path.join(TRIPOSR_DIR, "run.py")

def generate_image_from_prompt(prompt: str) -> None:
    """Generates a 2D image from a prompt using Imagen and saves it."""
    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        aspect_ratio="1:1",
        add_watermark=True,
    )

    pil_image = images[0]._pil_image
    os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)
    pil_image.save(IMAGE_PATH)
    print(f"[INFO] Image saved to {IMAGE_PATH}")

def run_tripoSR_inference(image_path: str = IMAGE_PATH) -> str:
    """Runs TripoSR’s 3D generation on the image."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    command = [
        "python3",
        TRIPOSR_RUN,
        image_path,
        "--output-dir",
        OUTPUT_DIR
    ]

    try:
        subprocess.run(command, check=True)
        print(f"[INFO] TripoSR successfully ran on {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] TripoSR failed: {e}")
        raise

    obj_output_path = os.path.join(OUTPUT_DIR, "0", "mesh.obj")
    if not os.path.exists(obj_output_path):
        raise FileNotFoundError("Expected output .obj file was not created.")

    return obj_output_path

def handle_prompt_to_obj(prompt: str) -> str:
    """Main FastAPI entry: prompt → image → TripoSR → .obj path."""
    generate_image_from_prompt(prompt)
    obj_path = run_tripoSR_inference()
    return obj_path
