# # This program will add visibile metadata (year/ professor) to each question.
# # To be applied to the questions table only.

# import mysql.connector
# import os

# def extract_metadata(question_id):
#     question_id = os.path.splitext(question_id)[0]
#     parts = question_id.split('_')
#     year = parts[0]
#     professor = f"Dr. {parts[1].capitalize()}"
#     return year, professor

# def update_table():
#     config = {
#         'user': 'Hemil',
#         'password': 'Hemil@TopicOverflow!',
#         'host': 'localhost',
#         'database': 'questra_production',
#     }

#     try:
#         conn = mysql.connector.connect(**config)
#         cursor = conn.cursor()
#         select_query = "SELECT id, question_id FROM questions_120"
#         cursor.execute(select_query)
#         rows = cursor.fetchall()

#         for row in rows:
#             id, question_id = row
#             year, professor = extract_metadata(question_id)
#             update_query = """
#             UPDATE questions 
#             SET year = %s, professor = %s 
#             WHERE id = %s
#             """
#             cursor.execute(update_query, (year, professor, id))

#         conn.commit()
#         print(f"Updated {cursor.rowcount} rows.")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")

#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()
#             print("MySQL connection is closed")

# if __name__ == "__main__":
#     update_table()
import mysql.connector
import os

def extract_metadata(question_id):
    # Remove file extension if present
    question_id = os.path.splitext(question_id)[0]
    parts = question_id.split('_')
    year = parts[0]
    professor = f"Dr. {parts[1].capitalize()}"
    return year, professor

def update_table():
    # Database connection configuration
    config = {
        'user': 'Hemil',
        'password': 'Hemil@TopicOverflow!',
        'host': 'localhost',
        'database': 'new_pairs456',
    }

    try:
        # Establish database connection
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Fetch all rows with question_id from questions_120
        select_query = "SELECT id, question_id FROM questions_456"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        # Update each row with the extracted year and professor
        for row in rows:
            id, question_id = row
            year, professor = extract_metadata(question_id)
            update_query = """
            UPDATE questions_456
            SET year = %s, professor = %s 
            WHERE id = %s
            """
            cursor.execute(update_query, (year, professor, id))

        # Commit the transaction
        conn.commit()
        print(f"Updated {cursor.rowcount} rows.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the database connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    update_table()
