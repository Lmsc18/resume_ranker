import os
from utils_ranker import pdf_to_images,docx_to_images,identify_resume,image_to_base64,delete_contents
from openai import OpenAI

client = OpenAI()



ocr_prompt="""You are an OCR (Optical Character Recognition) system tasked with parsing the content of an image and converting it into markdown format. The image content will be provided to you as text, describing what is visible in the image.

Your task is to interpret this image content and convert it into a well-formatted markdown representation. Follow these guidelines:

1. Identify the main elements in the image (text, headings, lists, tables, etc.).
2. Convert these elements into appropriate markdown syntax.
3. Preserve the structure and hierarchy of the content as much as possible.
4. If there are any visual elements like images or diagrams, represent them with appropriate markdown placeholders.

Use the following markdown conventions:
- Use # for headings (e.g., # Heading 1, ## Heading 2)
- Use - or * for unordered lists
- Use 1. 2. 3. for ordered lists
- Use | for tables
- Use `code` for inline code and ``` for code blocks
- Use > for blockquotes
- Use **bold** and *italic* for emphasis
- Use [text](url) for links
- Use ![alt text](image_url) for images

 Ensure that your output is a valid, well-formatted markdown representation of the image content."""

def read_resume(resume_name):
    delete_contents('resume_images')
    identify_resume(resume_name)
    resume_imgs=['resume_images/'+x for x in os.listdir('resume_images')] 
    content = []
    
    # Add image content for each path
    for path in resume_imgs:
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
        {"role": "system", "content": ocr_prompt},
        {"role": "user", "content": content}
    ],
    )
    markdown_resume=completion.choices[0].message.content
    name=os.path.splitext(resume_name)[0]
    with open(f"parsed_resumes/{name}.txt",'w',encoding='utf-8') as f:
        f.write(markdown_resume)
    

def parse_resumes():
    delete_contents("parsed_resumes")
    resume_list=os.listdir("resumes")
    for res in resume_list:
        read_resume(res)