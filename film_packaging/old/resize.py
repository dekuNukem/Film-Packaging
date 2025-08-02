import os
from PIL import Image

# Define the maximum allowed dimension
MAX_DIMENSION = 5000
SIZE_LIMIT_BYTES = 4 * 1024 * 1024  # 4MB in bytes

# Get all .jpg and .jpeg files in the current directory
image_files = [f for f in os.listdir('.') if f.lower().endswith(('.jpg', '.jpeg'))]

for file in image_files:
    try:
        
        # Skip if file size is under 4MB
        if os.path.getsize(file) < SIZE_LIMIT_BYTES:
            print(f"Skipped (under 4MB): {file}")
            continue

        with Image.open(file) as img:
            width, height = img.size
            max_dim = max(width, height)

            if max_dim > MAX_DIMENSION:
                # Calculate the scaling factor
                scale = MAX_DIMENSION / max_dim
                new_size = (int(width * scale), int(height * scale))
                
                # Resize and save the image
                img_resized = img.resize(new_size, Image.LANCZOS)
                img_resized.save(file, quality=90, optimize=True)
                print(f"Resized: {file} to {new_size}")
            else:
                img.save(file, quality=90, optimize=True)
                print(f"Re-saved at 90%: {file}")

    except Exception as e:
        print(f"Error processing {file}: {e}")
