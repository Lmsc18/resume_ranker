import os
from dotenv import load_dotenv
load_dotenv()

import uvicorn
from fastapi import FastAPI,UploadFile
from fastapi.responses import FileResponse
from typing import List
import shutil
from utils import delete_contents
from jd_extract import extract_criterias
from rank_resumes import rank_resumes

app = FastAPI()

UPLOAD_DIR = "resumes"  # Directory to store uploaded files
os.makedirs(UPLOAD_DIR, exist_ok=True) 

@app.post("/resume-ranker/get-jd-criterias",summary="Get Job Description criterias", description="Get the key criterias from a job description.")
async def get_criterias(file: UploadFile):
    prev_content = await file.read()
    filename = file.filename.lower()

    delete_contents("job_description")
    
    with open(f"job_description/{filename}", "wb") as f:
        f.write(prev_content)
    criterias=extract_criterias()
    return {"criterias":criterias}
    
@app.post("/resume-ranker/rank-resumes")
async def upload_files(files: List[UploadFile],criterias: List[str]):
    delete_contents("resumes")
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)
    rank_resumes(criteria=criterias)
    file_path="final_result/resume_results.xlsx"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        filename="resume_result.xlsx")
    return {"error": "File not found"}



if __name__ == "__main__":
    # Run the FastAPI application using uvicorn
    uvicorn.run(app,host="0.0.0.0", port=8005)