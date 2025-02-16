from docx2pdf import convert
from pdf2image import convert_from_path
import os
import base64
import shutil

def docx_to_images(docx_path, output_dir):
    # First convert DOCX to PDF
    pdf_path = docx_path.replace('.docx', '.pdf')
    convert(docx_path, pdf_path)
    
    # Then convert PDF to images
    images = convert_from_path(pdf_path,poppler_path="C:/poppler-24.02.0/Library/bin")
    
    # Save each page as an image
    for i, image in enumerate(images):
        image.save(os.path.join(output_dir, f'page_{i+1}.jpeg'))
    
    # Clean up the temporary PDF
    os.remove(pdf_path)

def pdf_to_images(pdf_path, output_folder, fmt='jpeg', dpi=200):
    """
    Convert a PDF to images (one per page).

    :param pdf_path: Path to the PDF file.
    :param output_folder: Folder to save the images.
    :param fmt: Image format (e.g., 'jpeg', 'png'). Default is 'jpeg'.
    :param dpi: DPI for the output images. Default is 200.
    :return: List of image file paths.
    """
    # Convert PDF to a list of images
    images = convert_from_path(pdf_path, dpi=dpi, fmt=fmt,poppler_path="C:/poppler-24.02.0/Library/bin")

    # Save images to the output folder
    image_paths = []
    for i, image in enumerate(images):
        image_path = f"{output_folder}/page_{i + 1}.{fmt}"
        image.save(image_path, fmt.upper())
        image_paths.append(image_path)

    return image_paths

def identify_jd(jd_name:str):
    if jd_name.endswith(".pdf"):
        pdf_to_images(f"job_description/{jd_name}","output_images")
    elif jd_name.endswith(".docx"):
        docx_to_images(f"job_description/{jd_name}","output_images")
    else:
        print("Job description file not supported.")

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
    return encoded_image

def delete_contents(folder_path):
    for item in os.listdir(folder_path):
        shutil.rmtree(os.path.join(folder_path, item)) if os.path.isdir(os.path.join(folder_path, item)) else os.unlink(os.path.join(folder_path, item))