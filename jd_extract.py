import os
from pydantic import BaseModel, Field
from typing import List
from utils import identify_jd,image_to_base64,delete_contents
from openai import OpenAI
client = OpenAI()

class Criteria(BaseModel):
    criteria: str = Field(description="criteria from the image JD")

class list_of_criterias(BaseModel):
    loc:List[Criteria]=Field(description="list of criterias")

jd_prompt="""
You are an AI assistant tasked with analyzing a job description image and extracting key ranking criterias. 
The image may contain multiple pages. 
Your goal is to carefully examine the image and identify the most important criteria for ranking candidates.

Note: Only add technical skills in the criterias

Example criterias:
1. Must have certification XYZ
2. 5+ years of experience in Python development
3. Strong background in Machine Learning
"""

def ocr(paths):
    # Create the base message content with the initial text
    content = [
        {
            "type": "text",
            "text": jd_prompt
        }
    ]
    
    # Add image content for each path
    for path in paths:
        image_data = image_to_base64(path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image_data}"
            }
        })
    completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}
    ],
    temperature=0.0,
    response_format=list_of_criterias)
    
    
    response=[x['criteria'] for x in completion.choices[0].message.parsed.model_dump()['loc']]
    return response

def extract_criterias():
    doc_name=os.listdir('job_description')[0]
    delete_contents('output_images')
    identify_jd(doc_name)
    image_list=["output_images/"+x for x in os.listdir('output_images')]
    criteria_list=ocr(image_list)
    return criteria_list