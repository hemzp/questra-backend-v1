# Integrates the topic name into the 'questions' table in the main DB. 
# Does this by accessing the metadata which was inputted in ClassifierUse.

import mysql.connector
from PIL import Image


# Function to extract metadata from the image
def extract_metadata_from_image(image_path):
    try:
        with Image.open(image_path) as img:
            metadata = img.info.get('Topic', None)
            return metadata
    except Exception as e:
        print(f"Error reading metadata from {image_path}: {e}")
        return None

# Function to update the topic in the database
def update_topic_in_db(cursor, question_id, topic):
    update_query = """
    UPDATE questions_456  # Replace this with your actual table name
    SET topic = %s
    WHERE question_id = %s
    """
    cursor.execute(update_query, (topic, question_id))

def process_images_from_db():
    # Connect to your database
    connection = mysql.connector.connect(
        host='localhost',
        user='Hemil',
        password='Hemil@TopicOverflow!',
        database='new_pairs456'
    )
    cursor = connection.cursor()

    # Fetch all file paths from the database
    cursor.execute("SELECT question_id, file_path FROM questions_456")  # Adjust table/column names as needed
    rows = cursor.fetchall()

    for question_id, file_path in rows:
        print(f"Processing question_id: {question_id}, file_path: {file_path}")
        
        # Extract metadata (topic) from the image file
        topic = extract_metadata_from_image(file_path)
        
        if topic:
            # Update the database with the extracted topic
            update_topic_in_db(cursor, question_id, topic)
            print(f"Updated database for question_id: {question_id}, Topic: {topic}")
        else:
            print(f"No topic metadata found for question_id: {question_id}")

    # Commit the changes to the database
    connection.commit()

    # Close the database connection
    cursor.close()
    connection.close()

# Example usage
process_images_from_db()
