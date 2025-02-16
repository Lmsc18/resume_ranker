import os
from pydantic import BaseModel, create_model, Field
from typing import Dict, Any, Type, Tuple, List
from resolve_criterias import resolve_criterias
from parse_resumes import parse_resumes
import pandas as pd
from openai import OpenAI

client = OpenAI()
def dynamic_pydantic_model(dynamic_fields: List[Dict[str, str]]) -> Type[BaseModel]:
    """
    Creates a dynamic Pydantic model with a permanent 'username' field and dynamic integer fields.

    :param dynamic_fields: List of dictionaries with 'property_name' and 'description'.
    :return: A dynamically generated Pydantic model class.
    """

    # Permanent field
    model_fields = {
        "Name": (str, Field(..., description="Name of the person in the resume"))
    }

    # Adding dynamic fields (all of type int)
    for field in dynamic_fields:
        property_name = field["criteria_name"]
        description = field["criteria_desc"]
        model_fields[property_name] = (int, Field(..., description=description))

    return create_model("DynamicModel", **model_fields)

sys_ranker="""
You are an Senior AI Resume Ranker. You have more than 30 years of experience in this field.
Given a resume and key criterias for ranking the resume, your role is to given a rank for the resume based on the key criterias.
The score of each criteria should be an integer between 0-5.
"""

ranker_template="""
Here is the resume:
{resume}
"""

def rank_resumes(criteria:list):
    parse_resumes()
    field_definitions=resolve_criterias(criteria)
    DynamicUserModel = dynamic_pydantic_model(field_definitions)
    parsed_resumes=["parsed_resumes/"+x for x in os.listdir("parsed_resumes")]
    final_results=[]
    for i in parsed_resumes:
        file=open(i,'r',encoding='utf-8').read()

        ranker_prompt=ranker_template.format(resume=file)
        completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_ranker},
            {"role": "user", "content": ranker_prompt}
        ],
        temperature=0.0,
        response_format=DynamicUserModel)
        out=completion.choices[0].message.parsed.model_dump()
        final_results.append(out)
    df=pd.DataFrame(final_results)
    df.to_excel("final_result/resume_results.xlsx",index=False)



