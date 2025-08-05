import os
from PIL import Image

MAX_DIMENSION = 5000
SIZE_LIMIT_BYTES = 4 * 1024 * 1024  # 4MB

target_dir = './to_add'

image_files = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.lower().endswith(('.jpg', '.jpeg'))]

if len(image_files) == 0:
    exit()

try:
    jpeg_quality = int(input("Enter JPEG quality (default 90): "))
except Exception:
    jpeg_quality = 90

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
                
                img_resized = img.resize(new_size, Image.LANCZOS)
                img_resized.save(file, quality=jpeg_quality, optimize=True)
                print(f"Resized: {file} to {new_size} at {jpeg_quality}% quality")
            else:
                img.save(file, quality=jpeg_quality, optimize=True)
                print(f"Re-saved {file} at {jpeg_quality}% quality")

    except Exception as e:
        print(f"Error processing {file}: {e}")
