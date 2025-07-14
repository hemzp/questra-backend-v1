import fitz
import os

class ExtractClass:
    def extract(self, filename, pdf_path, output_folder):
        print(f"Processing file: {filename}")
        
        try:
            # Open the PDF file
            pdf_document = fitz.open(pdf_path)
        except Exception as e:
            print(f"Error opening PDF file {pdf_path}: {e}")
            return
        
        page_number = 1  # Start page numbering from 1
        
        for i, page in enumerate(pdf_document):
            try:
                # Creating image of the page
                image = page.get_pixmap(matrix=fitz.Matrix(4, 4))
                
                # Constructing image name
                folder_name = os.path.basename(output_folder)
                image_name = f"{folder_name}_{page_number}.png"
                image_path = os.path.join(output_folder, image_name)
                
                image.save(image_path)
                print(f"Saved image: {image_path}")

                page_number += 1  # Increment page number only after saving image

            except Exception as e:
                print(f"Error processing page {i + 1}: {e}")
                # Do not increment page_number if there is an error

def process_head_folder(head_folder_path, output_head_folder):
    extracter = ExtractClass()
    
    for course_folder in os.listdir(head_folder_path):  # First loop: Iterate over course folders
        course_path = os.path.join(head_folder_path, course_folder)
        if os.path.isdir(course_path):
            print(f"Processing course: {course_folder}")
            
            output_course_folder = os.path.join(output_head_folder, "Math_Images_Answers_New", course_folder)
            os.makedirs(output_course_folder, exist_ok=True)
            
            for exam_folder in os.listdir(course_path): # Second loop: Iterate over all subfolders within a course (e.g., 'mid_1', 'mid_2', etc.)
                exam_path = os.path.join(course_path, exam_folder)
                if os.path.isdir(exam_path):
                    print(f"Processing exam: {exam_folder}")

                    output_exam_folder = os.path.join(output_course_folder, exam_folder)
                    os.makedirs(output_exam_folder, exist_ok=True)
                    
                    for filename in os.listdir(exam_path):  # Third loop: Iterate over files in each subfolder
                        if filename.endswith('.pdf'):
                            pdf_path = os.path.join(exam_path, filename) 
                            output_pdf_folder = os.path.join(output_exam_folder, os.path.splitext(filename)[0])
                            os.makedirs(output_pdf_folder, exist_ok=True)
                            extracter.extract(filename, pdf_path, output_pdf_folder)
                        else:
                            print(f"Skipping non-PDF file: {filename}")

# Example usage
head_folder_path = r'C:\Users\Hemil Patel\Desktop\Questra DB\Answers_PDF_New'  # Math_PDFs
output_head_folder = r'C:\Users\Hemil Patel\Desktop\Questra' # Base directory
process_head_folder(head_folder_path, output_head_folder)
