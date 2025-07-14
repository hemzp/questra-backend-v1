# Adds the answers to the 'answers' tables in the main DB.
# Iterates through the dir, adds course_name, answers_id, and file path.

import os
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="Hemil",
    password="Hemil@TopicOverflow!",
    database="new_pairs456"
)
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS answers_456 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255),
    answer_id VARCHAR(255),
    file_path TEXT
);
"""
cursor.execute(create_table_query)
conn.commit()
print("Table 'answers' ensured to exist.")

# Function to insert data into MySQL
def insert_question(course_name, question_id, file_path):
    query = "INSERT INTO answers_456 (course_name, answer_id, file_path) VALUES (%s, %s, %s)"
    cursor.execute(query, (course_name, question_id, file_path))
    conn.commit()
    print(f"Inserted: Course {course_name}, Answer ID {question_id}, File Path {file_path}")

# Start walking through the directory tree
base_dir = r'C:\Users\Hemil Patel\Desktop\Questra\Math_Images_Answers'
course_name = None

for root, dirs, files in os.walk(base_dir):
    # Extract folder name
    folder_name = os.path.basename(root)
    
    # Check if this folder represents a course (e.g., Math 124, Math 125, etc.)
    if folder_name.startswith('Math'):
        course_name = folder_name
        print(f"Identified course: {course_name}")
    
    # If we have already identified the course, now look for PNG files in subfolders
    for file in files:
        if file.endswith('.png'):
            file_path = os.path.join(root, file)
            answer_id = file  # Use the file name as question_id
            insert_question(course_name, answer_id, file_path)

# Close the MySQL connection
cursor.close()
conn.close()
