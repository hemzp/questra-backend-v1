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
CREATE TABLE IF NOT EXISTS questions_456 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255),
    year VARCHAR(255),
    topic VARCHAR(255),
    professor VARCHAR(225),
    question_id VARCHAR(255),
    file_path TEXT
);
"""
cursor.execute(create_table_query)
conn.commit()
print("Table 'questions_456' ensured to exist.")

# Function to insert data into MySQL with year and professor set to NULL
def insert_question(course_name, question_id, file_path):
    query = "INSERT INTO questions_456 (course_name, year, topic, professor, question_id, file_path) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (course_name, None, None, None, question_id, file_path))
    conn.commit()
    print(f"Inserted: Course {course_name}, Question ID {question_id}, File Path {file_path}")

# Start walking through the directory tree
base_dir = r'C:\Users\Hemil Patel\Desktop\Questra\456Main_Questions'
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
            question_id = file  # Use the file name as question_id
            insert_question(course_name, question_id, file_path)

# Close the MySQL connection
cursor.close()
conn.close()
