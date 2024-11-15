from langchain_community.llms import Ollama


class ModelHelper:

    @staticmethod
    def get_model(model="llama3.1"):
        return Ollama(model=model)
