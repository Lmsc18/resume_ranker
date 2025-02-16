# Resume Ranking System

## Overview
This project provides two API endpoints:
1. **Extracting Key Criteria from Job Description (JD)**
   - Upload a JD document.
   - Convert the JD to images.
   - Use an LLM to extract key/relevant criteria from the JD.

2. **Parsing and Ranking Resumes**
   - Upload resumes.
   - Upload extracted criteria.
   - Parse resumes into structured data.
   - Create a dynamic Pydantic class for validation.
   - Use an LLM to rank resumes based on extracted criteria.
   - Output the ranked resumes to an Excel file.

---

## **Installation Guide**

### **Step 1: Clone the Repository**
```sh
 git clone <repository_url>
 cd <repository_folder>
```

### **Step 2: Set Up a Virtual Environment (Optional but Recommended)**
```sh
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows
```

### **Step 3: Install Dependencies**
```sh
pip install -r requirements.txt
```

### **Step 4: Install Poppler (Required for PDF Processing)**

#### **Windows**
1. Download Poppler from: [https://github.com/oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)
2. Extract it and add the `bin` folder to the system `PATH`.

#### **MacOS**
```sh
brew install poppler
```

#### **Ubuntu/Debian**
```sh
sudo apt update
sudo apt install poppler-utils
```

#### **Arch Linux**
```sh
sudo pacman -S poppler
```

**After installing Poppler, make sure to update the Poppler path in the `utils.py` and `utils_ranker.py` files.**

---

## **Environment Variables**
Create a `.env` file in the root directory and add the following:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## **Running the Application**
```sh
python main.py
```

---

## **Usage**
### **Endpoint 1: Extracting Key Criteria from JD**
- Method: `POST`
- URL: `/extract_criteria`
- Payload: `{ "job_description": <JD_File> }`
- Response: `{ "criteria": ["Skill1", "Skill2", ...] }`

### **Endpoint 2: Parsing and Ranking Resumes**
- Method: `POST`
- URL: `/rank_resumes`
- Payload: `{ "resumes": [<Resume_Files>], "criteria": ["Skill1", "Skill2"] }`
- Response: `{ "ranked_resumes": <Excel_File> }`

---

## **Contributing**
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## **License**
MIT License

