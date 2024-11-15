from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chains import LLMChain

from model_helper import ModelHelper

import sys


class TimeConverter:

    def __init__(self, model):
        self.model = model

    def to_minutes(self, text):
        return self.extract_result(self.convert_time(text))

    def convert_time(self, text):
        system_prompt = f"""Please convert the time duration mentioned in the text into minutes.
                        Do the calculation step by step, and then output the final result."""
        return self.get_response(text, system_prompt)

    def extract_result(self, text):
        system_prompt = f"""Please extract the number in the final result and 
                        output nothing else but that number with digits only."""
        return int(self.get_response(text, system_prompt).replace(",", ""))

    def get_response(self, message, system_prompt):
        prompt = self.get_prompt(system_prompt)
        conversation = LLMChain(
            llm=self.model,
            prompt=prompt,
        )
        return conversation.predict(input=message)

    def get_prompt(self, system_prompt):
        messages = [SystemMessagePromptTemplate.from_template(system_prompt)]
        messages.append(HumanMessagePromptTemplate.from_template("{input}"))

        return ChatPromptTemplate(messages=messages)


if __name__ == "__main__":
    text = sys.argv[1]
    converter = TimeConverter(ModelHelper.get_model())
    convert_result = converter.convert_time(text)
    result_number = converter.extract_result(convert_result)

    print(convert_result)
    print(result_number)
    print(converter.to_minutes(text))
