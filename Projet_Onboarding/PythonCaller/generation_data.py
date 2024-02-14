from typing import List

from dataclasses import dataclass

from llm_core.assistants import OpenAIAssistant 

import pandas as pd 

model = "gpt-3.5-turbo"

@dataclass
class Instruction:
    instruction : str
    instruction_class : str

@dataclass
class InstructionsData:
    system_prompt= "You are a generator of relevant data based on user queries."

    prompt = """
#Goal
Give me a very large number of very varied User Instructions that can be categorized in different classes such as analysis, summary, translation, generation, explanation etc. 
Be creative and as close to reality as possible, the requests and labels must be in French.

#Context
These instructions will be used to create a database for a classification model. 

#Exemple :
[Instructition : Traduis moi cette partie du  texte en Anglais 
instrutction_class: Traduire]
[instruction : Résume moi ce texte, le résultat doit etre en 3 points principaux détaillant chacune des parties
instruction_class: Résumer ]

#Quantity 
I need {number} Instuctions. stocked in my instructions list
"""
    
    instructions : List[Instruction]


class Generator: 
    def generate_data(self, number):
        with OpenAIAssistant(InstructionsData, model) as assistant:
            resp = assistant.process(number=number)
            datas = assistant.process(number=number)
            return datas


generator = Generator()
new_datas = generator.generate_data(number=50)

data_to_save = [{'Instruction': inst.instruction , 'Class': inst.instruction_class} for inst in new_datas.instructions]
df = pd.DataFrame(data_to_save)
print(df)
csv_file_path = 'data100.csv'
df.to_csv(csv_file_path, index=False,encoding='utf-8')
