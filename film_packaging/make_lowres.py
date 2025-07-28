import os
from PIL import Image

# Define the source and destination directories
archive_folder = './archive'
lowres_folder = './lowres'

# Create the lowres folder if it doesn't exist
if not os.path.exists(lowres_folder):
    os.makedirs(lowres_folder)

max_width = 800

# Loop through all files in the archive folder
for filename in os.listdir(archive_folder):
    if filename.lower().endswith('.jpg'):
        output_path = os.path.join(lowres_folder, filename)
        # Skip processing if the file already exists
        if os.path.exists(output_path):
            print(f"Skipped {filename} - already exists.")
            continue

        # Full path of the source file
        file_path = os.path.join(archive_folder, filename)
        # Open the image
        with Image.open(file_path) as img:
            if img.width > max_width:
                # Calculate the new height preserving the aspect ratio
                new_width = max_width
                new_height = int((new_width / img.width) * img.height)
                
                # Resize the image
                img = img.resize((new_width, new_height))

            # Save the resized image to the lowres folder
            output_path = os.path.join(lowres_folder, filename)
            img.save(output_path)

        print(f"Resized {filename} and saved to {output_path}")
