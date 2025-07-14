from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
import json
import os
import io
import base64
import time
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
import openai

# Set OpenAI API key
openai.api_key = 'sike'

class JSONTopicProvider:
    def __init__(self, json_file):
        with open(json_file, 'r') as file:
            self.topics = json.load(file)

    def get_topics(self, course, exam_type):
        return self.topics.get(f'{course}_{exam_type}', {})


class QuestionClassifier:
    def __init__(self, image_path, topic_provider, course, exam_type, log_file='log1.txt'):
        self.image_path = image_path
        self.topic_provider = topic_provider
        self.course = course
        self.exam_type = exam_type
        self.log_file = log_file
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained("facebook/nougat-base")
        self.model = AutoModelForVision2Seq.from_pretrained("facebook/nougat-base").to(self.device)

    def fetch_image(self):
        
        image = Image.open(self.image_path)
        return image    

    def extract_latex_from_image(self):
        # Process the image
        image = self.fetch_image()
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        start_time = time.time()
        outputs = self.model.generate(**inputs, max_new_tokens=300, num_beams=3, early_stopping=True)
        generated_text = self.processor.batch_decode(outputs, skip_special_tokens=True)[0]
        end_time = time.time()
        print(f"LaTeX Extraction Time: {end_time - start_time:.2f} seconds")
        return generated_text
    
    def classify(self):
        latex_text = self.extract_latex_from_image()
        context = self.topic_provider.get_topics(self.course, self.exam_type)  # Pass course and exam_type
        context_text = "\n".join(
            [f"{topic}:\nDescription: {info['description']}\nKeywords: {', '.join(info['keywords'])}" 
             for topic, info in context.items()]
        )
        try:
            response = openai.chat.completions.create(
                model='gpt-4o',
                messages=[ 
                    {"role": "system", "content": "You are an expert in classifying academic questions into specific topics. And a expert in LaTeX reading and understanding."},
                    {"role": "user", "content": f"""Classify the following question, using its LaTeX text, into one of the topics based on the provided context. Each topic includes a detailed description and relevant keywords. Please match the given question to the most appropriate topic.
     
     Context:
     {context_text}

     LaTeX Text:
     {latex_text}

     Please provide the topic classification only in plain text, without any additional explanation."""}
                ],
                temperature=0.0,
            )
            message = response.choices[0].message.content
            topic = message.strip('"').strip("'")
        except (KeyError, IndexError, AttributeError) as e:
            print(f"Error in response format: {e}")
            topic = "Unclassified"
        with open(self.log_file, 'a', encoding='utf-8') as log:
            log.write(f"Classified Topic: {topic}\n")
            log.write("="*50 + "\n")
        return topic



def add_text_to_image(image_path, text, position=(100, 100), color="black", font_path="arial.ttf", font_size=36):
    # Open the image file
    image = Image.open(image_path)
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)
    
    # Define the font
    font = ImageFont.truetype(font_path, size=font_size)  # You can change the font and size
    
    # Add text to the image
    draw.text(position, text, fill=color, font=font)
    
    # Save the edited image
    image.save(image_path)  # Save over the same file
    print(f"Text added to image and saved: {image_path}")

def add_metadata_to_image(image_path, classified_topic):
    # Open the image file
    image = Image.open(image_path)
    
    # Add metadata to the image
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Topic", classified_topic)
    
    # Save the image with metadata (overwriting the same file)
    image.save(image_path, "PNG", pnginfo=meta)
    print(f"Metadata added to image and saved: {image_path}")

def process_folder(head_folder_path, log_file_path, json_folder_path):
    for course_folder in os.listdir(head_folder_path):
        course_path = os.path.join(head_folder_path, course_folder)
        
        if os.path.isdir(course_path):
            course = os.path.basename(course_path)
            json_file_name = f'{course}.json'  # Adjusted to match 'Math 120.json'
            json_file_path = os.path.join(json_folder_path, json_file_name)

            print(f"Course folder: {course_folder}")
            print(f"Constructed JSON file name: {json_file_name}")
            print(f"Constructed JSON file path: {json_file_path}")
            
            # Check if the JSON file exists
            if not os.path.exists(json_file_path):
                print(f"JSON file for course {course} not found: {json_file_path}")
                continue

            print(f"Processing course: {course} with JSON: {json_file_path}")
            topic_provider = JSONTopicProvider(json_file_path)
            
            # Go into each midterm or exam folder within the course folder
            for exam_folder in os.listdir(course_path):
                exam_path = os.path.join(course_path, exam_folder)
                
                if os.path.isdir(exam_path):
                    exam_type = os.path.basename(exam_path)
                    print(f"Processing exam type: {exam_type}")
                    
                    # Start walking through the directory tree
                    for root, dirs, files in os.walk(exam_path):
                        for image_file in files:
                            if image_file.lower().endswith('.png'):
                                image_path = os.path.join(root, image_file)
                                
                                # Classify the image using QuestionClassifier
                                classifier = QuestionClassifier(
                                    image_path=image_path,
                                    topic_provider=topic_provider,
                                    course=course,
                                    exam_type=exam_type,
                                    log_file=log_file_path
                                )
                                topic = classifier.classify()
                                
                                # Add text to the image
                                add_text_to_image(image_path, f"Topic: {topic}", position=(100, 100), color="black", font_path="arial.ttf", font_size=36)
                                
                                # Add metadata to the image
                                add_metadata_to_image(image_path, topic)
                            else:
                                print(f"Skipping non-image file: {image_file}")

# Example usage
head_folder_path = r'C:\Users\Hemil Patel\Desktop\Questra\test'
log_file_path = r'C:\Users\Hemil Patel\Desktop\classification_log.txt'
json_folder_path = r'C:\Users\Hemil Patel\Desktop\Questra\Classification\Topics Update'
process_folder(head_folder_path, log_file_path, json_folder_path)
