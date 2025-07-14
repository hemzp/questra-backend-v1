import os
import logging
import mysql.connector

# Configure the logger
logging.basicConfig(filename='file_matching6.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Root directories for questions and answers
questions_root = r'C:\Users\Hemil Patel\Desktop\Questra\456Main_Questions'
answers_root = r'C:\Users\Hemil Patel\Desktop\Questra\Math_Images_Answers'

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'Hemil',
    'password': 'Hemil@TopicOverflow!',
    'database': 'new_pairs456'
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        logging.info("Connected to the database successfully.")
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to the database: {err}")
        return None

def create_table_if_not_exists(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS pairs_456 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question_file VARCHAR(255) NOT NULL,
        answer_file VARCHAR(255) NOT NULL
    )
    """
    cursor.execute(create_table_query)
    logging.info("Table 'pairs_456' checked/created successfully.")

def insert_matched_pair(cursor, question_file, answer_file):
    insert_query = """
    INSERT INTO pairs_456 (question_file, answer_file)
    VALUES (%s, %s)
    """
    cursor.execute(insert_query, (question_file, answer_file))

def list_dir(path):
    dirs, files = [], []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            dirs.append(entry)
        else:
            files.append(entry)
    return sorted(dirs), sorted(files)

def get_file_number(filename):
    # Extracts the number part from the filename (assumes format like 'something_number.png')
    return int(filename.split('_')[-1].split('.')[0])

def sanitize_folder_name(name):
    # Remove '_sol' or any other suffix that might differ between question and answer folders
    return name.replace('_sol', '').strip()

def recursive_traverse(q_path, a_path, cursor):
    q_dirs, q_files = list_dir(q_path)
    a_dirs, a_files = list_dir(a_path)

    matched_pairs = []

    # Normalize folder names for comparison
    q_dirs_normalized = [sanitize_folder_name(d) for d in q_dirs]
    a_dirs_normalized = [sanitize_folder_name(d) for d in a_dirs]

    # Log directories being compared
    logging.info(f"Comparing directories:\nQuestion directories: {q_dirs_normalized}\nAnswer directories: {a_dirs_normalized}")

    # Check if the directory structures are consistent
    if sorted(q_dirs_normalized) != sorted(a_dirs_normalized):
        logging.error(f"Directory structure mismatch between '{q_path}' and '{a_path}'.")
        logging.error(f"Question directories: {q_dirs_normalized}")
        logging.error(f"Answer directories: {a_dirs_normalized}")
        return matched_pairs

    # Recursively traverse subdirectories
    for q_dir, a_dir in zip(q_dirs, a_dirs):
        # Extend matched_pairs with results from deeper recursive calls
        matched_pairs.extend(recursive_traverse(
            os.path.join(q_path, q_dir),
            os.path.join(a_path, a_dir),
            cursor
        ))

    # Match files based on the end numbers
    q_file_map = {get_file_number(qf): qf for qf in q_files}
    a_file_map = {get_file_number(af): af for af in a_files}

    # Log file comparison information
    logging.info(f"Matching files in '{q_path}' and '{a_path}'")
    logging.info(f"Question files: {list(q_file_map.values())}")
    logging.info(f"Answer files: {list(a_file_map.values())}")

    for num in q_file_map:
        if num in a_file_map:
            question_file = os.path.join(q_path, q_file_map[num])
            answer_file = os.path.join(a_path, a_file_map[num])
            matched_pairs.append((question_file, answer_file))
            insert_matched_pair(cursor, question_file, answer_file)  # Insert into database
        else:
            logging.warning(f"No matching answer found for question file '{q_file_map[num]}' in '{q_path}'.")

    for num in a_file_map:
        if num not in q_file_map:
            logging.warning(f"No matching question found for answer file '{a_file_map[num]}' in '{a_path}'.")

    return matched_pairs

def main():
    # Connect to the database
    connection = connect_to_database()
    if connection is None:
        logging.error("Terminating the script due to database connection issues.")
        return
    
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    create_table_if_not_exists(cursor)

    # Run the traversal and matching
    matched_pairs = recursive_traverse(questions_root, answers_root, cursor)

    # Commit the changes to the database
    connection.commit()

    # Log the matched pairs for verification
    for question_file, answer_file in matched_pairs:
        logging.info(f"Matched Question: {question_file} with Answer: {answer_file}")

    # Close the cursor and connection
    cursor.close()
    connection.close()
    logging.info("File matching completed.")

if __name__ == "__main__":
    main()
