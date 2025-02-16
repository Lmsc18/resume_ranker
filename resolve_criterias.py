import os
from pydantic import BaseModel,Field
from openai import OpenAI

class criteria(BaseModel):
    criteria_name:str=Field(description="shortened criteria from the criteria. It should be short enough for a column name")
    criteria_desc:str=Field(description="short description of the criteria")
class criteria_list(BaseModel):
    list_of_criteria:list[criteria]=Field(description="List of criteria from the given criterias")

client = OpenAI()

sys_prompt="""
You are an AI Assistant whose task is to extract a shortened criteria and criteria description from the given criterias.
You are given a list of criterias. 
"""
human_template="""
Here are the criterias:
{crts}
"""

def resolve_criterias(criterias:list):
    human_prompt=human_template.format(crts=criterias)
    completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": human_prompt}
    ],
    response_format=criteria_list)
    field_definitions=completion.choices[0].message.parsed.model_dump()['list_of_criteria']
    return field_definitions