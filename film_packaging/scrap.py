import os
import sys
from PIL import Image

def convert_png_to_jpeg(directory_path):
    if not os.path.isdir(directory_path):
        print(f"The provided path '{directory_path}' is not a directory.")
        return

    # Iterate over all files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.lower().endswith('.png'):
            # Full path to the file
            file_path = os.path.join(directory_path, file_name)
            try:
                # Open the image
                with Image.open(file_path) as img:
                    # Convert to RGB (JPEG does not support alpha channel)
                    rgb_img = img.convert('RGB')
                    # Replace .png with .jpeg for the output file name
                    jpeg_file_name = os.path.splitext(file_name)[0] + '.jpeg'
                    jpeg_file_path = os.path.join(directory_path, jpeg_file_name)
                    # Save the image as JPEG with 90% quality
                    rgb_img.save(jpeg_file_path, 'JPEG', quality=90)
                    print(f"Converted '{file_name}' to '{jpeg_file_name}'")
            except Exception as e:
                print(f"Failed to convert '{file_name}': {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python convert_png_to_jpeg.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        convert_png_to_jpeg(directory_path)
