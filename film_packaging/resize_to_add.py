import os
from PIL import Image

MAX_DIMENSION = 6500
SIZE_LIMIT_BYTES = 4 * 1024 * 1024  # 4MB

target_dir = './to_add'

# Accept .jpg, .jpeg, and .png
image_files = [
    os.path.join(target_dir, f)
    for f in os.listdir(target_dir)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
]

if len(image_files) == 0:
    exit()

DEFAULT_JPEG_QUALITY = 80

try:
    jpeg_quality = int(input(f"Enter JPEG quality (default {DEFAULT_JPEG_QUALITY}): "))
except Exception:
    jpeg_quality = DEFAULT_JPEG_QUALITY

for file in image_files:
    try:
        if os.path.getsize(file) < SIZE_LIMIT_BYTES:
            print(f"Skipped (under 4MB): {file}")
            continue

        with Image.open(file) as img:
            width, height = img.size
            max_dim = max(width, height)

            if max_dim > MAX_DIMENSION:
                scale = MAX_DIMENSION / max_dim
                new_size = (int(width * scale), int(height * scale))
                img = img.resize(new_size, Image.LANCZOS)

            # Ensure RGB (JPEG doesn't support transparency or palette)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Always save as JPEG (overwrite original file with .jpg extension)
            out_file = os.path.splitext(file)[0] + ".jpg"
            img.save(out_file, "JPEG", quality=jpeg_quality, optimize=True)

            print(f"Processed {file} -> {out_file} ({img.size}) at {jpeg_quality}% quality")

        # If original was a PNG, delete it after successful conversion
        if file.lower().endswith(".png"):
            os.remove(file)
            print(f"Deleted original PNG: {file}")

    except Exception as e:
        print(f"Error processing {file}: {e}")
