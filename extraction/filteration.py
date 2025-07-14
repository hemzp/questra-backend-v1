import os
from PIL import Image
import pytesseract

# Step 1: OCR the images
def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Step 2: Filter out irrelevant images and plain white images
def is_irrelevant(image_path):
    text = ocr_image(image_path).lower()
    keywords = ["signature", "scratch", "student id", "instructions", "selected formulas", "student number"]
    
    for keyword in keywords:
        if keyword in text:
            print(f"Image {os.path.basename(image_path)} is irrelevant due to keyword: {keyword}")
            return True
    
    if is_plain_white(text):
        print(f"Image {os.path.basename(image_path)} is plain white or contains no text.")
        return True
    
    return False

# Step 3: Check if the image has no text after OCR
def is_plain_white(text):
    return not text.strip()

# Step 4: Process images in a nested directory structure
def process_images_in_folder(root_dir, log_file_path):
    with open(log_file_path, 'a') as log_file:
        for dirpath, _, filenames in os.walk(root_dir):
            # Sort and filter out non-image files before processing
            images = sorted(f for f in filenames if f.endswith(('.png', '.jpg', '.jpeg')))

            deleted_count = 0

            for i, image_name in enumerate(images):
                image_path = os.path.join(dirpath, image_name)
                
                if is_irrelevant(image_path):
                    try:
                        os.remove(image_path)
                        deleted_count += 1
                        print(f"Deleted {image_name} in {dirpath}")
                    except Exception as e:
                        error_message = f"Error: Could not delete {image_name} in {dirpath} due to {str(e)}"
                        print(error_message)
                        log_file.write(f"{error_message}\n")
                else:
                    base_name, ext = os.path.splitext(image_name)
                    parts = base_name.split('_')
                    parts[-1] = str(i + 1 - deleted_count)  # Adjusting the page number
                    
                    new_base_name = '_'.join(parts)
                    new_name = f'{new_base_name}{ext}'
                    
                    new_path = os.path.join(dirpath, new_name)
                    
                    if new_path != image_path:
                        try:
                            os.rename(image_path, new_path)
                            print(f"Renamed {image_name} to {new_name} in {dirpath}")
                        except FileExistsError:
                            error_message = f"Error: Cannot rename {image_name} to {new_name} in {dirpath}. File already exists."
                            print(error_message)
                            log_file.write(f"{error_message}\n")
                        except Exception as e:
                            error_message = f"Error: Could not rename {image_name} to {new_name} in {dirpath} due to {str(e)}"
                            print(error_message)
                            log_file.write(f"{error_message}\n")

    print("Processing complete!")

# Replace this with the root directory path where your three folders are located
root_dir = r'C:\Users\Hemil Patel\Desktop\Questra\Math_Images_Answers_New'

# Specify the path for the log file
log_file_path = r'C:\Users\Hemil Patel\Desktop\Questra\log1.txt'

# Process all images in the nested directory structure and log errors
process_images_in_folder(root_dir, log_file_path)
