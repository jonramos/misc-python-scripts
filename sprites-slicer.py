import cv2
import numpy as np
import zipfile
import os

def extract_and_zip_sprites(image_path, output_zip):
    # Load the image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not load {image_path}")
        return

    # Assume the top-left pixel is the background color
    bg_color = img[0, 0]
    
    # Create a mask of all pixels that are NOT the background color
    # If the image has an alpha channel, we also check for transparency
    if img.shape[2] == 4:
        # BGR channels match background OR alpha is 0
        mask_bg = np.all(img[:, :, :3] == bg_color[:3], axis=-1) | (img[:, :, 3] == 0)
    else:
        mask_bg = np.all(img == bg_color, axis=-1)
        
    mask_fg = (~mask_bg).astype(np.uint8) * 255

    # Find contours (the boundaries of each sprite)
    contours, _ = cv2.findContours(mask_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    sprite_filenames = []
    
    # Create a temporary directory or just save files locally before zipping
    if not os.path.exists('temp_sprites'):
        os.makedirs('temp_sprites')

    # Extract each sprite
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter out tiny noise (e.g., text artifacts or 1x1 pixels)
        if w > 5 and h > 5:
            sprite = img[y:y+h, x:x+w]
            filename = f"temp_sprites/sprite_{i+1}.png"
            cv2.imwrite(filename, sprite)
            sprite_filenames.append(filename)

    # Zip the extracted sprites
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for file in sprite_filenames:
            zipf.write(file, os.path.basename(file))
            os.remove(file) # Clean up the image after zipping

    os.rmdir('temp_sprites')
    print(f"Successfully extracted {len(sprite_filenames)} sprites and saved to {output_zip}")

# Run the extraction
extract_and_zip_sprites("card-icons.png", "extracted_sprites.zip")