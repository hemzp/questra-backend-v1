# **Questra \- Back-End Workflow**

## **Overview**

[Questra](https://questra-ai.com/) is a software application designed to extract, classify, and store university past paper questions and answers in a structured database. This document outlines the original workflow of the back-end processes involved in automating the extraction, classification, and storage of questions and answers, along with cloud storage integration.

## **Table of Contents**

1. Prerequisites  
2. Extraction Process  
3. Classification Process  
4. Database Management  
5. Cloud Integration  
6. Directory Structure  
7. Execution Instructions  
8. Future Improvements

---

## **Prerequisites**

Ensure the following software and libraries are installed to run the Questra back-end:

* **Python 3.8+**  
* **MySQL** for database management  
* **AWS CLI** for S3 integration  
* **Required Python Packages**:  
  * Extraction Process:  
    * `pymupdf for pdf to png`  
    * `pillow image library`  
  * `Classification: (AI/ML Libraries)`  
    * `torch`  
    * `transformers`  
    * `openai`  
    * `pytesseract` for OCR processing  
    * `requests` for API communication (GPT models)  
  * DB Management:  
    * `boto3` for AWS S3 interaction  
    * `mysql-connector-python` for MySQL database connections

---

## **Extraction Process**

### **1\. ExtractClassMain**

The `ExtractClassMain.py` script is responsible for extracting questions from past paper PDFs. It processes each PDF file, converting pages into images and saving each question page in a separate folder for future classification.

* **Input**: PDF file containing past paper.  
* **Output**: Extracted question images saved in a specified folder.

### **2\. AnswerExtractClass**

`AnswerExtractClass.py` extends the functionality of `ExtractClassMain` by adding additional features:

* **Input**: PDF file containing answer papers.  
* **Output**: Extracted answer images saved in a specified folder.

### **3\. filtration**

`filtration.py` filters out plain white pages and irrelevant pages from the Answers Images folder.

* Filters irrelevant answer pages (e.g., blank pages, scratch pages).  
* Renumbers the pictures in the answer files to ensure naming conventions  
* **Input**: PDF file containing answer papers.  
* **Output**: Filtered answer images saved in a specified folder.

---

## **Classification Process**

### **3\. Classifier**

The `Classifier.py` file handles the classification of each extracted question based on the course topics.

#### **Workflow:**

* **OCR Processing**: Uses the [**Facebook Nougat Model**](https://github.com/facebookresearch/nougat) to convert each question image to LaTeX text format.  
* **GPT-based Classification**: The extracted text is then passed to a GPT-based API, which matches the question to a specific topic based on the course.  
* **Output**: The classified question is moved to a folder named according to its topic.  
* **Input**: Extracted question images.  
* **Output**: Classified question images with topic as their metadata.

---

## 

## 

## **Database Management**

### **4\. add\_question\_to+db**

This file is responsible for adding each extracted question into the `questions` table within the MySQL database. It stores metadata such as the course, question ID and file\_path.

* **Input**: Extracted questions.  
* **Output**: Metadata entries in the `questions` table.

### **5\. insert\_metadata**

Handles the insertion of additional metadata related to each question, including:

* Professor  
* Year

This program updates the metadata of each question after classification.

### **6\. ClassifieDBadd**

Once the question is classified, this script updates the `questions` table with the correct topic based on the GPT classification.

* **Input**: Classified question images.  
* **Output**: Database entries with topics assigned to each question.

### **7\. add\_answers\_to\_db**

This program adds the extracted and filtered answer images into the `answers` table in the MySQL database.

Columns:

* Course  
* Answer ID  
* File Path

* **Input**: Extracted answer images.  
* **Output**: Answer image entries in the `answers` table.

### **8\. newTraverser**

The `newTraverser.py` script uses a recursive function to match each question to its respective answer in the database by leveraging the folder structure. The recursive function creates a new table `pairs`, where each question is linked to the correct answer.

* **Input**: Question and answer metadata.  
* **Output**: A `pairs` table mapping each question to its answer.

---

## **Cloud Integration**

### **9\. cloud\_test1.py**

This file manages the uploading of both question and answer images to an AWS S3 bucket. After uploading, it updates the `question_file_path` and `answer_file_path` fields in the `pairs` table to point to the S3 bucket links.

* **Input**: Local image paths for questions and answers.  
* **Output**: Updated database entries with S3 links to the images.

### **AWS S3 Bucket Structure**

The images are stored in the following format:

`/year/professor/course/exam_type/question_images/`  
`/year/professor/course/exam_type/answer_images/`

---

## **Directory Structure**

Below is the original file structure for the Questra back-end:

bash  
Copy code  
`questra_backend/`  
`├── extraction/`  
`│   ├── ExtractClassMain.py`  
`│   └── AnswerExtractClass.py`  
`├── classification/`  
`│   └── Classifier.py`  
`├── database/`  
`│   ├── add_question_to+db.py`  
`│   ├── insert_metadata.py`  
`│   ├── ClassifieDBadd.py`  
`│   ├── add_answers_to_db.py`  
`│   └── newTraverser.py`  
`├── cloud/`  
`│   └── cloud_test1.py`  
`└── README.md`

---

## 
---

## **Future Improvements**

While this workflow is functional, several improvements can be made in future versions:


---

## **Contact Information**

For any queries, contact Hemil at hemilpats@gmail.com.

