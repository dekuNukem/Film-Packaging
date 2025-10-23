import os
from PIL import Image

DEFAULT_MAX_DIMENSION = 6500
SIZE_LIMIT_BYTES = 4 * 1024 * 1024  # 4MB
DEFAULT_JPEG_QUALITY = 80

target_dir = './to_add'

def rename_jpeg_to_jpg(dir_path):
    for filename in os.listdir(dir_path):
        if filename.lower().endswith('.jpeg'):
            old_path = os.path.join(dir_path, filename)
            new_filename = filename[: -5] + '.jpg'  # remove '.jpeg', add '.jpg'
            new_path = os.path.join(dir_path, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

rename_jpeg_to_jpg(target_dir)

image_files = [
    os.path.join(target_dir, f)
    for f in os.listdir(target_dir)
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff'))
]

if len(image_files) == 0:
    exit()

# Ask for JPEG quality
try:
    jpeg_quality = int(input(f"Enter JPEG quality (default {DEFAULT_JPEG_QUALITY}): ").strip() or DEFAULT_JPEG_QUALITY)
except Exception:
    jpeg_quality = DEFAULT_JPEG_QUALITY

# Ask for max dimension
try:
    max_dimension = int(input(f"Enter max dimension (default {DEFAULT_MAX_DIMENSION}): ").strip() or DEFAULT_MAX_DIMENSION)
except Exception:
    max_dimension = DEFAULT_MAX_DIMENSION

for file in image_files:
    print(file)
    try:
        if (str(file).lower().endswith((".jpg", '.jpeg'))) and os.path.getsize(file) < SIZE_LIMIT_BYTES:
            print(f"Skipped (under 4MB): {file}")
            continue

        with Image.open(file) as img:
            width, height = img.size
            max_dim = max(width, height)

            if max_dim > max_dimension:
                scale = max_dimension / max_dim
                new_size = (int(width * scale), int(height * scale))
                img = img.resize(new_size, Image.LANCZOS)

            # Ensure RGB (JPEG doesn't support transparency or palette)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Always save as JPEG (overwrite original file with .jpg extension)
            out_file = os.path.splitext(file)[0] + ".jpg"
            img.save(out_file, "JPEG", quality=jpeg_quality, optimize=True)

            print(f"Processed {file} -> {out_file} ({img.size}) at {jpeg_quality}% quality")

        # If original was a PNG/TIFF, delete it after successful conversion
        if file.lower().endswith(('.png', '.tif', '.tiff')):
            os.remove(file)
            print(f"Deleted original: {file}")

    except Exception as e:
        print(f"Error processing {file}: {e}")
